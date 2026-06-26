package cmd

import (
	"fmt"
	"strings"
	"sync"
	"time"

	"github.com/maxtechera/admirarr/internal/api"
	"github.com/maxtechera/admirarr/internal/arr"
	"github.com/maxtechera/admirarr/internal/config"
	"github.com/maxtechera/admirarr/internal/qbit"
	"github.com/maxtechera/admirarr/internal/seerr"
	"github.com/maxtechera/admirarr/internal/ui"
	"github.com/spf13/cobra"
)

var statusLive bool
var statusInterval int

var statusCmd = &cobra.Command{
	Use:   "status",
	Short: "Dashboard: services, library, queues, requests, disk",
	Long: `Fleet dashboard — full stack status at a glance.

Shows services, library stats, Seerr requests, *Arr queues, active tasks,
qBittorrent downloads, and disk usage. All API calls run in parallel for speed.

Use --live for auto-refreshing mode.`,
	Example: "  admirarr status\n  admirarr status --live\n  admirarr status --live --interval 10",
	Run:     runStatus,
}

func init() {
	statusCmd.Flags().BoolVar(&statusLive, "live", false, "Auto-refresh the dashboard")
	statusCmd.Flags().IntVar(&statusInterval, "interval", 5, "Refresh interval in seconds (with --live)")
	rootCmd.AddCommand(statusCmd)
}

func runStatus(cmd *cobra.Command, args []string) {
	if statusLive && !ui.IsJSON() {
		if err := runStatusTUI(); err != nil {
			fmt.Printf("  %s\n", ui.Err(fmt.Sprintf("TUI error: %v", err)))
		}
	} else {
		renderDashboard()
	}
}

// ── Collected data from parallel fetches ──

type dashData struct {
	mu sync.Mutex

	// Services
	serviceUp map[string]bool
	serviceMs map[string]int64

	// Library (from Radarr/Sonarr)
	movies    []arr.Movie
	moviesErr bool
	series    []arr.Series
	seriesErr bool

	// Jellyfin counts
	jellyfinCounts *jellyfinItemCounts
	jellyfinErr    bool

	// Health
	healthItems []statusHealthItem

	// Queues
	radarrQueue statusQueueData
	sonarrQueue statusQueueData

	// Torrents
	torrents    []qbit.Torrent
	torrentsErr bool

	// Seerr requests
	seerrRequests []seerr.Request
	seerrTotal    int
	seerrErr      bool

	// Indexers
	prowlarrIndexers []statusIndexer
	indexersErr      bool

	// Activity
	commands []statusCommandInfo

	// Disk
	diskTotal int64
	diskFree  int64
	diskErr   bool
}

type jellyfinItemCounts struct {
	MovieCount   int `json:"MovieCount"`
	SeriesCount  int `json:"SeriesCount"`
	EpisodeCount int `json:"EpisodeCount"`
}
type statusHealthItem struct {
	Svc     string
	Type    string `json:"type"`
	Message string `json:"message"`
}
type statusQueueData struct {
	Total   int
	Records []arr.QueueRecord
	Err     bool
}
type statusCommandInfo struct {
	Svc    string
	Name   string `json:"name"`
	Status string `json:"status"`
}
type statusIndexer struct {
	Name   string `json:"name"`
	Enable bool   `json:"enable"`
}

func renderDashboard() {
	d := &dashData{
		serviceUp: make(map[string]bool),
		serviceMs: make(map[string]int64),
	}

	// Phase 1: Probe all services across candidate hosts in parallel.
	// This also updates in-memory hosts so Phase 2 API calls use the right address.
	probed := config.ProbeAll()
	var wg sync.WaitGroup
	for name, ss := range probed {
		d.serviceUp[name] = ss.Up
		d.serviceMs[name] = ss.LatencyMs
	}

	// Phase 2: Fetch all data in parallel (only from reachable services)
	fetch := func(fn func()) {
		wg.Add(1)
		go func() { defer wg.Done(); fn() }()
	}

	if d.serviceUp["radarr"] {
		radarrClient := arr.New("radarr")
		fetch(func() {
			movies, err := radarrClient.Movies()
			if err != nil {
				d.moviesErr = true
			} else {
				d.movies = movies
			}
		})
		fetch(func() {
			page, err := radarrClient.Queue(10)
			if err != nil {
				d.radarrQueue.Err = true
			} else {
				d.radarrQueue.Total = page.TotalRecords
				d.radarrQueue.Records = page.Records
			}
		})
		fetch(func() {
			items, err := radarrClient.Health()
			if err == nil {
				var tagged []statusHealthItem
				for _, item := range items {
					tagged = append(tagged, statusHealthItem{Svc: "radarr", Type: item.Type, Message: item.Message})
				}
				d.mu.Lock()
				d.healthItems = append(d.healthItems, tagged...)
				d.mu.Unlock()
			}
		})
		fetch(func() {
			cmds, err := radarrClient.Commands()
			if err == nil {
				var tagged []statusCommandInfo
				for _, c := range cmds {
					tagged = append(tagged, statusCommandInfo{Svc: "radarr", Name: c.Name, Status: c.Status})
				}
				d.mu.Lock()
				d.commands = append(d.commands, tagged...)
				d.mu.Unlock()
			}
		})
	}

	if d.serviceUp["sonarr"] {
		sonarrClient := arr.New("sonarr")
		fetch(func() {
			series, err := sonarrClient.Series()
			if err != nil {
				d.seriesErr = true
			} else {
				d.series = series
			}
		})
		fetch(func() {
			page, err := sonarrClient.Queue(10)
			if err != nil {
				d.sonarrQueue.Err = true
			} else {
				d.sonarrQueue.Total = page.TotalRecords
				d.sonarrQueue.Records = page.Records
			}
		})
		fetch(func() {
			items, err := sonarrClient.Health()
			if err == nil {
				var tagged []statusHealthItem
				for _, item := range items {
					tagged = append(tagged, statusHealthItem{Svc: "sonarr", Type: item.Type, Message: item.Message})
				}
				d.mu.Lock()
				d.healthItems = append(d.healthItems, tagged...)
				d.mu.Unlock()
			}
		})
		fetch(func() {
			cmds, err := sonarrClient.Commands()
			if err == nil {
				var tagged []statusCommandInfo
				for _, c := range cmds {
					tagged = append(tagged, statusCommandInfo{Svc: "sonarr", Name: c.Name, Status: c.Status})
				}
				d.mu.Lock()
				d.commands = append(d.commands, tagged...)
				d.mu.Unlock()
			}
		})
	}

	if d.serviceUp["prowlarr"] {
		prowlarrClient := arr.New("prowlarr")
		fetch(func() {
			items, err := prowlarrClient.Health()
			if err == nil {
				var tagged []statusHealthItem
				for _, item := range items {
					tagged = append(tagged, statusHealthItem{Svc: "prowlarr", Type: item.Type, Message: item.Message})
				}
				d.mu.Lock()
				d.healthItems = append(d.healthItems, tagged...)
				d.mu.Unlock()
			}
		})
		fetch(func() {
			var idxs []statusIndexer
			indexers, err := prowlarrClient.Indexers()
			if err != nil {
				d.indexersErr = true
			} else {
				for _, idx := range indexers {
					idxs = append(idxs, statusIndexer{Name: idx.Name, Enable: idx.Enable})
				}
				d.prowlarrIndexers = idxs
			}
		})
	}

	if d.serviceUp["jellyfin"] {
		fetch(func() {
			var counts jellyfinItemCounts
			if err := api.GetJSON("jellyfin", "Items/Counts", nil, &counts); err != nil {
				d.jellyfinErr = true
			} else {
				d.jellyfinCounts = &counts
			}
		})
	}

	if d.serviceUp["qbittorrent"] {
		fetch(func() {
			torrents, err := qbit.New().Torrents()
			if err != nil {
				d.torrentsErr = true
			} else {
				d.torrents = torrents
			}
		})
	}

	if d.serviceUp["seerr"] {
		fetch(func() {
			page, err := seerr.New().Requests(8)
			if err != nil {
				d.seerrErr = true
			} else {
				d.seerrRequests = page.Results
				d.seerrTotal = page.PageInfo.Results
			}
		})
	}

	// Disk (local, fast)
	fetch(func() {
		total, free, err := getStatfs(config.DataPath())
		if err != nil {
			d.diskErr = true
		} else {
			d.diskTotal = total
			d.diskFree = free
		}
	})

	wg.Wait()

	// ── JSON output ──
	if ui.IsJSON() {
		type serviceJSON struct {
			Name    string `json:"name"`
			Host    string `json:"host"`
			Up      bool   `json:"up"`
			Ms      int64  `json:"latency_ms"`
			Runtime string `json:"runtime"`
		}
		type libraryJSON struct {
			Movies       int   `json:"movies"`
			MoviesOnDisk int   `json:"movies_on_disk"`
			Shows        int   `json:"shows"`
			Episodes     int   `json:"episodes"`
			EpisodeFiles int   `json:"episode_files"`
			TotalSize    int64 `json:"total_size"`
		}
		type requestJSON struct {
			Status int    `json:"status"`
			Is4K   bool   `json:"is_4k"`
			User   string `json:"user"`
		}
		type queueItemJSON struct {
			Title string  `json:"title"`
			State string  `json:"state"`
			Size  float64 `json:"size"`
		}
		type torrentJSON struct {
			Name     string  `json:"name"`
			Size     int64   `json:"size"`
			Progress float64 `json:"progress"`
			DLSpeed  int64   `json:"dl_speed"`
			State    string  `json:"state"`
		}
		type diskJSON struct {
			Total int64 `json:"total"`
			Free  int64 `json:"free"`
		}
		type indexerJSON struct {
			Name    string `json:"name"`
			Enabled bool   `json:"enabled"`
		}
		type indexersSummaryJSON struct {
			Configured  int            `json:"configured"`
			Enabled     int            `json:"enabled"`
			Recommended int            `json:"recommended"`
			Missing     []string       `json:"missing"`
			Indexers    []indexerJSON   `json:"indexers"`
		}
		type statusOut struct {
			Services []serviceJSON          `json:"services"`
			Library  libraryJSON            `json:"library"`
			Health   []statusHealthItem     `json:"health"`
			Indexers *indexersSummaryJSON    `json:"indexers,omitempty"`
			Requests []requestJSON          `json:"requests"`
			Queues   struct {
				Radarr []queueItemJSON `json:"radarr"`
				Sonarr []queueItemJSON `json:"sonarr"`
			} `json:"queues"`
			Torrents []torrentJSON `json:"torrents"`
			Disk     *diskJSON     `json:"disk,omitempty"`
		}

		out := statusOut{}
		for _, name := range config.AllServiceNames() {
			def, _ := config.GetServiceDef(name)
			if def.Port == 0 {
				continue
			}
			ss := probed[name]
			out.Services = append(out.Services, serviceJSON{Name: name, Host: ss.Host, Up: ss.Up, Ms: ss.LatencyMs, Runtime: ss.Runtime.Label})
		}
		lib := libraryJSON{}
		if !d.moviesErr && d.movies != nil {
			lib.Movies = len(d.movies)
			for _, m := range d.movies {
				if m.HasFile {
					lib.MoviesOnDisk++
				}
				lib.TotalSize += m.SizeOnDisk
			}
		}
		if !d.seriesErr && d.series != nil {
			lib.Shows = len(d.series)
			for _, s := range d.series {
				lib.Episodes += s.Statistics.EpisodeCount
				lib.EpisodeFiles += s.Statistics.EpisodeFileCount
				lib.TotalSize += s.Statistics.SizeOnDisk
			}
		}
		out.Library = lib
		out.Health = d.healthItems
		if out.Health == nil {
			out.Health = []statusHealthItem{}
		}
		for _, r := range d.seerrRequests {
			out.Requests = append(out.Requests, requestJSON{Status: r.Status, Is4K: r.Is4K, User: r.RequestedBy.DisplayName})
		}
		if out.Requests == nil {
			out.Requests = []requestJSON{}
		}
		for _, rec := range d.radarrQueue.Records {
			out.Queues.Radarr = append(out.Queues.Radarr, queueItemJSON{Title: rec.Title, State: rec.TrackedDownloadState, Size: rec.Size})
		}
		if out.Queues.Radarr == nil {
			out.Queues.Radarr = []queueItemJSON{}
		}
		for _, rec := range d.sonarrQueue.Records {
			out.Queues.Sonarr = append(out.Queues.Sonarr, queueItemJSON{Title: rec.Title, State: rec.TrackedDownloadState, Size: rec.Size})
		}
		if out.Queues.Sonarr == nil {
			out.Queues.Sonarr = []queueItemJSON{}
		}
		for _, t := range d.torrents {
			out.Torrents = append(out.Torrents, torrentJSON{Name: t.Name, Size: t.Size, Progress: t.Progress, DLSpeed: t.DLSpeed, State: t.State})
		}
		if out.Torrents == nil {
			out.Torrents = []torrentJSON{}
		}
		if !d.diskErr {
			out.Disk = &diskJSON{Total: d.diskTotal, Free: d.diskFree}
		}
		if !d.indexersErr && d.serviceUp["prowlarr"] {
			idxSummary := &indexersSummaryJSON{
				Recommended: len(recommendedIndexers),
			}
			configuredNames := make(map[string]bool)
			for _, idx := range d.prowlarrIndexers {
				idxSummary.Indexers = append(idxSummary.Indexers, indexerJSON{Name: idx.Name, Enabled: idx.Enable})
				configuredNames[strings.ToLower(idx.Name)] = true
				if idx.Enable {
					idxSummary.Enabled++
				}
			}
			idxSummary.Configured = len(d.prowlarrIndexers)
			for _, rec := range recommendedIndexers {
				if !configuredNames[strings.ToLower(rec.Name)] {
					idxSummary.Missing = append(idxSummary.Missing, rec.Name)
				}
			}
			if idxSummary.Missing == nil {
				idxSummary.Missing = []string{}
			}
			if idxSummary.Indexers == nil {
				idxSummary.Indexers = []indexerJSON{}
			}
			out.Indexers = idxSummary
		}
		ui.PrintJSON(out)
		return
	}

	// ── Render ──
	now := time.Now().Format("15:04:05")
	fmt.Printf("\n  %s %s %s    %s  %s\n",
		ui.GoldText("⚓"), ui.Bold("ADMIRARR"), ui.Dim("v"+ui.Version),
		ui.Dim("Command your fleet."), ui.Dim(now))
	fmt.Println(ui.Separator())

	// Services (compact 2-column)
	fmt.Printf("\n  %s\n", ui.Bold("Fleet"))
	names := config.AllServiceNames()
	for _, name := range names {
		def, _ := config.GetServiceDef(name)
		if def.Port == 0 {
			continue
		}
		ss := probed[name]
		host := ss.Host
		addr := fmt.Sprintf(":%d", config.ServicePort(name))
		if host != "" && host != "localhost" && host != "127.0.0.1" {
			addr = fmt.Sprintf("%s:%d", host, config.ServicePort(name))
		}
		rtLabel := "  " + ui.Dim(ss.Runtime.Label)
		if ss.Up {
			fmt.Printf("  %s %-13s%s %s%s\n", ui.Ok("●"), name,
				ui.Dim(addr),
				ui.Dim(fmt.Sprintf("%dms", ss.LatencyMs)),
				rtLabel)
		} else {
			fmt.Printf("  %s %-13s%s %s%s\n", ui.Err("○"), name,
				ui.Dim(addr),
				ui.Err("down"),
				rtLabel)
		}
	}

	// Indexers
	fmt.Printf("\n  %s\n", ui.Bold("Indexers"))
	if !d.indexersErr && d.serviceUp["prowlarr"] {
		configuredNames := make(map[string]bool)
		enabled, disabled := 0, 0
		for _, idx := range d.prowlarrIndexers {
			configuredNames[strings.ToLower(idx.Name)] = true
			if idx.Enable {
				enabled++
			} else {
				disabled++
			}
		}
		var missing []string
		for _, rec := range recommendedIndexers {
			if !configuredNames[strings.ToLower(rec.Name)] {
				missing = append(missing, rec.Name)
			}
		}
		have := len(recommendedIndexers) - len(missing)
		total := len(recommendedIndexers)
		if len(missing) == 0 {
			fmt.Printf("  %s %d/%d recommended\n", ui.Ok("✓"), have, total)
		} else {
			fmt.Printf("  %s %d/%d recommended — missing: %s\n",
				ui.Warn("⚠"), have, total, strings.Join(missing, ", "))
		}
		summary := fmt.Sprintf("%d configured, %d enabled", len(d.prowlarrIndexers), enabled)
		if disabled > 0 {
			summary += fmt.Sprintf(", %d disabled", disabled)
		}
		fmt.Printf("  %s\n", ui.Dim(summary))
	} else {
		fmt.Printf("  %s\n", ui.Dim("unavailable"))
	}

	// Library
	fmt.Printf("\n  %s\n", ui.Bold("Library"))

	// Jellyfin counts
	if d.jellyfinCounts != nil {
		fmt.Printf("  %s  %d movies, %d series, %d episodes\n",
			ui.GoldText("Jellyfin"), d.jellyfinCounts.MovieCount, d.jellyfinCounts.SeriesCount, d.jellyfinCounts.EpisodeCount)
	}

	if !d.moviesErr && d.movies != nil {
		have, missing := 0, 0
		var totalSize int64
		for _, m := range d.movies {
			if m.HasFile {
				have++
			}
			if m.Monitored && !m.HasFile {
				missing++
			}
			totalSize += m.SizeOnDisk
		}
		missStr := ui.Ok("0 missing")
		if missing > 0 {
			missStr = ui.Err(fmt.Sprintf("%d missing", missing))
		}
		fmt.Printf("  %s     %d total, %s, %s  %s\n",
			ui.GoldText("Movies"), len(d.movies), ui.Ok(fmt.Sprintf("%d on disk", have)), missStr, ui.Dim(ui.FmtSize(totalSize)))
	} else {
		fmt.Printf("  %s     %s\n", ui.GoldText("Movies"), ui.Dim("unavailable"))
	}
	if !d.seriesErr && d.series != nil {
		totalEps, haveEps := 0, 0
		var totalSize int64
		for _, s := range d.series {
			totalEps += s.Statistics.EpisodeCount
			haveEps += s.Statistics.EpisodeFileCount
			totalSize += s.Statistics.SizeOnDisk
		}
		fmt.Printf("  %s   %d shows, %s  %s\n",
			ui.GoldText("TV Shows"), len(d.series), ui.Ok(fmt.Sprintf("%d/%d episodes", haveEps, totalEps)), ui.Dim(ui.FmtSize(totalSize)))
	} else {
		fmt.Printf("  %s   %s\n", ui.GoldText("TV Shows"), ui.Dim("unavailable"))
	}

	// Requests
	fmt.Printf("\n  %s", ui.Bold("Requests"))
	if d.seerrTotal > 0 {
		fmt.Printf(" %s\n", ui.Dim(fmt.Sprintf("(%d)", d.seerrTotal)))
	} else {
		fmt.Println()
	}
	if !d.seerrErr && len(d.seerrRequests) > 0 {
		for _, r := range d.seerrRequests {
			title, year := resolveTitle(r.Media.MediaType, r.Media.TmdbID)
			status := statusNames[r.Status]
			icon, colorFn := "○", ui.Dim
			switch r.Status {
			case 4:
				icon = "●"
				colorFn = ui.Ok
			case 2:
				icon = "◐"
				colorFn = ui.Warn
			case 1:
				icon = "○"
				colorFn = ui.GoldText
			}
			if len(title) > 42 {
				title = title[:42] + "…"
			}
			s4k := ""
			if r.Is4K {
				s4k = " 4K"
			}
			fmt.Printf("  %s %-12s %s (%s)%s\n", colorFn(icon), colorFn(status), title, year, s4k)
		}
	} else if !d.seerrErr {
		fmt.Printf("  %s\n", ui.Dim("No requests"))
	} else {
		fmt.Printf("  %s\n", ui.Dim("Seerr unavailable"))
	}

	// Activity
	activeCount := 0
	for _, c := range d.commands {
		if c.Status == "started" || c.Status == "queued" {
			activeCount++
		}
	}
	if activeCount > 0 {
		fmt.Printf("\n  %s\n", ui.Bold("Activity"))
		for _, c := range d.commands {
			if c.Status == "started" || c.Status == "queued" {
				icon := ui.Warn("⟳")
				if c.Status == "queued" {
					icon = ui.Dim("◷")
				}
				fmt.Printf("  %s %s %s %s\n", icon, ui.Dim("["+c.Svc+"]"), c.Name, ui.Dim(c.Status))
			}
		}
	}

	// Health
	if len(d.healthItems) > 0 {
		fmt.Printf("\n  %s\n", ui.Bold("Health"))
		for _, item := range d.healthItems {
			level := ui.Warn("WARN")
			if item.Type == "error" {
				level = ui.Err("ERROR")
			}
			msg := item.Message
			if len(msg) > 60 {
				msg = msg[:60] + "…"
			}
			fmt.Printf("  %s %s %s\n", level, ui.Dim("["+item.Svc+"]"), msg)
		}
	}

	// Queues
	hasQueue := d.radarrQueue.Total > 0 || d.sonarrQueue.Total > 0
	if hasQueue {
		fmt.Printf("\n  %s\n", ui.Bold("Queues"))
		for _, q := range []struct {
			name string
			data statusQueueData
		}{
			{"radarr", d.radarrQueue},
			{"sonarr", d.sonarrQueue},
		} {
			for _, rec := range q.data.Records {
				colorFn := ui.Err
				if rec.TrackedDownloadState == "downloading" {
					colorFn = ui.Ok
				} else if rec.TrackedDownloadState == "importPending" {
					colorFn = ui.Warn
				}
				title := rec.Title
				if len(title) > 45 {
					title = title[:45] + "…"
				}
				pct := ""
				if rec.Size > 0 {
					p := (1 - rec.Sizeleft/rec.Size) * 100
					pct = ui.Dim(fmt.Sprintf(" %.0f%%", p))
				}
				fmt.Printf("  %s %-14s %s%s\n", ui.Dim("["+q.name+"]"), colorFn(rec.TrackedDownloadState), title, pct)
			}
		}
	}

	// Torrents
	if d.torrents != nil {
		dlStates := map[string]bool{"downloading": true, "stalledDL": true, "forcedDL": true, "metaDL": true}
		seedStates := map[string]bool{"uploading": true, "stalledUP": true, "forcedUP": true}
		var dlCount, seedCount int
		var totalDL int64
		for _, t := range d.torrents {
			if dlStates[t.State] {
				dlCount++
				totalDL += t.DLSpeed
			}
			if seedStates[t.State] {
				seedCount++
			}
		}
		fmt.Printf("\n  %s\n", ui.Bold("Torrents"))
		if dlCount > 0 {
			for _, t := range d.torrents {
				if !dlStates[t.State] {
					continue
				}
				pct := int(t.Progress * 100)
				speed := float64(t.DLSpeed) / 1048576
				name := t.Name
				if len(name) > 40 {
					name = name[:40] + "…"
				}
				barLen := 12
				filled := barLen * pct / 100
				bar := strings.Repeat("█", filled) + strings.Repeat("░", barLen-filled)
				eta := fmtETA(t.ETA)
				fmt.Printf("  [%s] %s %s  %s %s\n",
					bar, ui.GoldText(fmt.Sprintf("%3d%%", pct)),
					fmt.Sprintf("%.1f MB/s", speed), name, ui.Dim(eta))
			}
		}
		fmt.Printf("  %s\n", ui.Dim(fmt.Sprintf(
			"%d downloading (%.1f MB/s), %d seeding, %d total",
			dlCount, float64(totalDL)/1048576, seedCount, len(d.torrents))))
	}

	// Disk
	if !d.diskErr {
		used := d.diskTotal - d.diskFree
		pct := float64(used) / float64(d.diskTotal) * 100
		barLen := 20
		filled := int(float64(barLen) * pct / 100)
		bar := strings.Repeat("█", filled) + strings.Repeat("░", barLen-filled)
		colorFn := ui.Ok
		if pct >= 90 {
			colorFn = ui.Err
		} else if pct >= 80 {
			colorFn = ui.Warn
		}
		fmt.Printf("\n  %s  [%s] %s  %s free / %s\n",
			ui.Bold("Disk"), bar, colorFn(fmt.Sprintf("%.0f%%", pct)),
			ui.FmtSize(d.diskFree), ui.FmtSize(d.diskTotal))
	}
	fmt.Println()
}

func fmtETA(secs int64) string {
	if secs <= 0 || secs > 8640000 {
		return ""
	}
	if secs < 60 {
		return fmt.Sprintf("%ds", secs)
	}
	if secs < 3600 {
		return fmt.Sprintf("%dm%ds", secs/60, secs%60)
	}
	return fmt.Sprintf("%dh%dm", secs/3600, (secs%3600)/60)
}
