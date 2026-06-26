package cmd

import (
	"fmt"
	"strings"
	"sync"
	"time"

	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"
	"github.com/maxtechera/admirarr/internal/api"
	"github.com/maxtechera/admirarr/internal/arr"
	"github.com/maxtechera/admirarr/internal/config"
	"github.com/maxtechera/admirarr/internal/qbit"
	"github.com/maxtechera/admirarr/internal/seerr"
	"github.com/maxtechera/admirarr/internal/ui"
)

// ── Messages ──

type tickMsg time.Time

type serviceResult struct {
	Name string
	Up   bool
	Ms   int64
}

type moviesResult struct {
	Movies []arr.Movie
	Err    bool
}

type seriesResult struct {
	Series []arr.Series
	Err    bool
}

type jellyfinCountsResult struct {
	Counts *jellyfinItemCounts
	Err    bool
}

type healthResult struct {
	Items []statusHealthItem
}

type queueResult struct {
	Svc     string
	Total   int
	Records []arr.QueueRecord
}

type torrentsResult struct {
	Torrents []qbit.Torrent
	Err      bool
}

type seerrResult struct {
	Requests []seerr.Request
	Total    int
	Titles   map[int]titleInfo // tmdbID -> title
	Err      bool
}

type titleInfo struct {
	Title string
	Year  string
}

type commandsResult struct {
	Commands []statusCommandInfo
}

type indexersResult struct {
	Indexers []statusIndexer
	Err      bool
}

type diskResult struct {
	Total int64
	Free  int64
	Err   bool
}

// ── Model ──

type tuiModel struct {
	width  int
	height int

	// Data
	services       map[string]serviceResult
	movies         *moviesResult
	series         *seriesResult
	jellyfinCounts *jellyfinCountsResult
	health         *healthResult
	radarrQueue    *queueResult
	sonarrQueue    *queueResult
	torrents       *torrentsResult
	seerr          *seerrResult
	commands       *commandsResult
	indexers       *indexersResult
	disk           *diskResult

	// State
	loading    bool
	lastUpdate time.Time
	tick       int
	quitting   bool
}

func newTuiModel() tuiModel {
	return tuiModel{
		services: make(map[string]serviceResult),
		loading:  true,
	}
}

func (m tuiModel) Init() tea.Cmd {
	return tea.Batch(
		tea.EnterAltScreen,
		fetchAll(),
		tickCmd(),
	)
}

func tickCmd() tea.Cmd {
	return tea.Tick(5*time.Second, func(t time.Time) tea.Msg {
		return tickMsg(t)
	})
}

// fetchAll fires all API calls concurrently, returns results as messages.
func fetchAll() tea.Cmd {
	return func() tea.Msg {
		var msgs []tea.Msg
		var mu sync.Mutex
		var wg sync.WaitGroup

		addMsg := func(m tea.Msg) {
			mu.Lock()
			msgs = append(msgs, m)
			mu.Unlock()
		}

		// Services
		for _, name := range config.AllServiceNames() {
			def, _ := config.GetServiceDef(name)
			if def.Port == 0 {
				continue
			}
			wg.Add(1)
			go func(n string) {
				defer wg.Done()
				t0 := time.Now()
				up := api.CheckReachable(n)
				ms := time.Since(t0).Milliseconds()
				addMsg(serviceResult{Name: n, Up: up, Ms: ms})
			}(name)
		}

		// Movies
		wg.Add(1)
		go func() {
			defer wg.Done()
			movies, err := arr.New("radarr").Movies()
			addMsg(moviesResult{Movies: movies, Err: err != nil})
		}()

		// Series
		wg.Add(1)
		go func() {
			defer wg.Done()
			series, err := arr.New("sonarr").Series()
			addMsg(seriesResult{Series: series, Err: err != nil})
		}()

		// Jellyfin counts
		wg.Add(1)
		go func() {
			defer wg.Done()
			var counts jellyfinItemCounts
			err := api.GetJSON("jellyfin", "Items/Counts", nil, &counts)
			addMsg(jellyfinCountsResult{Counts: &counts, Err: err != nil})
		}()

		// Health
		wg.Add(1)
		go func() {
			defer wg.Done()
			var items []statusHealthItem
			for _, svc := range []string{"radarr", "sonarr", "prowlarr"} {
				h, err := arr.New(svc).Health()
				if err == nil {
					for _, item := range h {
						items = append(items, statusHealthItem{Svc: svc, Type: item.Type, Message: item.Message})
					}
				}
			}
			addMsg(healthResult{Items: items})
		}()

		// Queues
		for _, svc := range []string{"radarr", "sonarr"} {
			wg.Add(1)
			go func(s string) {
				defer wg.Done()
				page, _ := arr.New(s).Queue(10)
				if page != nil {
					addMsg(queueResult{Svc: s, Total: page.TotalRecords, Records: page.Records})
				} else {
					addMsg(queueResult{Svc: s})
				}
			}(svc)
		}

		// Torrents
		wg.Add(1)
		go func() {
			defer wg.Done()
			torrents, err := qbit.New().Torrents()
			addMsg(torrentsResult{Torrents: torrents, Err: err != nil})
		}()

		// Seerr
		wg.Add(1)
		go func() {
			defer wg.Done()
			client := seerr.New()
			page, err := client.Requests(8)
			if err != nil {
				addMsg(seerrResult{Err: true})
				return
			}
			// Resolve titles in parallel
			titles := make(map[int]titleInfo)
			var tmu sync.Mutex
			var twg sync.WaitGroup
			for _, r := range page.Results {
				twg.Add(1)
				go func(mediaType string, tmdbID int) {
					defer twg.Done()
					t, y := client.ResolveTitle(mediaType, tmdbID)
					tmu.Lock()
					titles[tmdbID] = titleInfo{Title: t, Year: y}
					tmu.Unlock()
				}(r.Media.MediaType, r.Media.TmdbID)
			}
			twg.Wait()
			addMsg(seerrResult{Requests: page.Results, Total: page.PageInfo.Results, Titles: titles})
		}()

		// Indexers (Prowlarr)
		wg.Add(1)
		go func() {
			defer wg.Done()
			indexers, err := arr.New("prowlarr").Indexers()
			var idxs []statusIndexer
			if err == nil {
				for _, idx := range indexers {
					idxs = append(idxs, statusIndexer{Name: idx.Name, Enable: idx.Enable})
				}
			}
			addMsg(indexersResult{Indexers: idxs, Err: err != nil})
		}()

		// Commands
		wg.Add(1)
		go func() {
			defer wg.Done()
			var all []statusCommandInfo
			for _, svc := range []string{"radarr", "sonarr"} {
				cmds, err := arr.New(svc).Commands()
				if err == nil {
					for _, c := range cmds {
						all = append(all, statusCommandInfo{Svc: svc, Name: c.Name, Status: c.Status})
					}
				}
			}
			addMsg(commandsResult{Commands: all})
		}()

		// Disk
		wg.Add(1)
		go func() {
			defer wg.Done()
			total, free, err := getStatfs(config.DataPath())
			addMsg(diskResult{Total: total, Free: free, Err: err != nil})
		}()

		wg.Wait()
		return batchResults(msgs)
	}
}

type batchResults []tea.Msg

func (m tuiModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch msg := msg.(type) {
	case tea.KeyMsg:
		switch msg.String() {
		case "q", "ctrl+c", "esc":
			m.quitting = true
			return m, tea.Quit
		case "r":
			m.loading = true
			return m, fetchAll()
		}

	case tea.WindowSizeMsg:
		m.width = msg.Width
		m.height = msg.Height

	case tickMsg:
		m.tick++
		m.loading = true
		return m, tea.Batch(fetchAll(), tickCmd())

	case batchResults:
		var cmds []tea.Cmd
		for _, sub := range msg {
			var cmd tea.Cmd
			updated, cmd := m.Update(sub)
			m = updated.(tuiModel)
			if cmd != nil {
				cmds = append(cmds, cmd)
			}
		}
		m.loading = false
		m.lastUpdate = time.Now()
		return m, tea.Batch(cmds...)

	case serviceResult:
		m.services[msg.Name] = msg
	case moviesResult:
		m.movies = &msg
	case seriesResult:
		m.series = &msg
	case jellyfinCountsResult:
		m.jellyfinCounts = &msg
	case healthResult:
		m.health = &msg
	case queueResult:
		if msg.Svc == "radarr" {
			m.radarrQueue = &msg
		} else {
			m.sonarrQueue = &msg
		}
	case torrentsResult:
		m.torrents = &msg
	case seerrResult:
		m.seerr = &msg
	case commandsResult:
		m.commands = &msg
	case indexersResult:
		m.indexers = &msg
	case diskResult:
		m.disk = &msg
	}

	return m, nil
}

func (m tuiModel) View() string {
	if m.quitting {
		return ""
	}

	var b strings.Builder

	// Header
	spinner := "●"
	if m.loading {
		frames := []string{"◐", "◓", "◑", "◒"}
		spinner = ui.GoldText(frames[m.tick%4])
	} else {
		spinner = ui.Ok("●")
	}
	ts := m.lastUpdate.Format("15:04:05")
	if m.lastUpdate.IsZero() {
		ts = "loading…"
	}

	b.WriteString(fmt.Sprintf("\n  %s %s %s    %s  %s  %s\n",
		ui.GoldText("⚓"), ui.Bold("ADMIRARR"), ui.Dim("v"+ui.Version),
		ui.Dim("Command your fleet."), ui.Dim(ts), spinner))
	b.WriteString(ui.Separator() + "\n")

	// Fleet
	b.WriteString(fmt.Sprintf("\n  %s\n", ui.Bold("Fleet")))
	names := config.AllServiceNames()
	// Filter out portless services
	var displayNames []string
	for _, n := range names {
		def, _ := config.GetServiceDef(n)
		if def.Port > 0 {
			displayNames = append(displayNames, n)
		}
	}
	// Render 2 columns
	for i := 0; i < len(displayNames); i += 2 {
		left := renderServiceCell(m.services, displayNames[i])
		right := ""
		if i+1 < len(displayNames) {
			right = renderServiceCell(m.services, displayNames[i+1])
		}
		b.WriteString(fmt.Sprintf("  %-38s%s\n", left, right))
	}

	// Indexers
	b.WriteString(fmt.Sprintf("\n  %s\n", ui.Bold("Indexers")))
	if m.indexers != nil && !m.indexers.Err {
		configuredNames := make(map[string]bool)
		enabled, disabled := 0, 0
		for _, idx := range m.indexers.Indexers {
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
			b.WriteString(fmt.Sprintf("  %s %d/%d recommended\n", ui.Ok("✓"), have, total))
		} else {
			b.WriteString(fmt.Sprintf("  %s %d/%d recommended — missing: %s\n",
				ui.Warn("⚠"), have, total, strings.Join(missing, ", ")))
		}
		summary := fmt.Sprintf("%d configured, %d enabled", len(m.indexers.Indexers), enabled)
		if disabled > 0 {
			summary += fmt.Sprintf(", %d disabled", disabled)
		}
		b.WriteString(fmt.Sprintf("  %s\n", ui.Dim(summary)))
	} else {
		b.WriteString(fmt.Sprintf("  %s\n", ui.Dim("…")))
	}

	// Library
	b.WriteString(fmt.Sprintf("\n  %s\n", ui.Bold("Library")))

	// Jellyfin counts
	if m.jellyfinCounts != nil && !m.jellyfinCounts.Err {
		c := m.jellyfinCounts.Counts
		b.WriteString(fmt.Sprintf("  %s  %d movies, %d series, %d episodes\n",
			ui.GoldText("Jellyfin"), c.MovieCount, c.SeriesCount, c.EpisodeCount))
	}

	if m.movies != nil && !m.movies.Err {
		have, missing := 0, 0
		var sz int64
		for _, mv := range m.movies.Movies {
			if mv.HasFile {
				have++
			}
			if mv.Monitored && !mv.HasFile {
				missing++
			}
			sz += mv.SizeOnDisk
		}
		missStr := ui.Ok("0 missing")
		if missing > 0 {
			missStr = ui.Err(fmt.Sprintf("%d missing", missing))
		}
		b.WriteString(fmt.Sprintf("  %s     %d total, %s, %s  %s\n",
			ui.GoldText("Movies"), len(m.movies.Movies), ui.Ok(fmt.Sprintf("%d on disk", have)), missStr, ui.Dim(ui.FmtSize(sz))))
	} else {
		b.WriteString(fmt.Sprintf("  %s     %s\n", ui.GoldText("Movies"), ui.Dim("…")))
	}
	if m.series != nil && !m.series.Err {
		te, he := 0, 0
		var sz int64
		for _, s := range m.series.Series {
			te += s.Statistics.EpisodeCount
			he += s.Statistics.EpisodeFileCount
			sz += s.Statistics.SizeOnDisk
		}
		b.WriteString(fmt.Sprintf("  %s   %d shows, %s  %s\n",
			ui.GoldText("TV Shows"), len(m.series.Series), ui.Ok(fmt.Sprintf("%d/%d episodes", he, te)), ui.Dim(ui.FmtSize(sz))))
	} else {
		b.WriteString(fmt.Sprintf("  %s   %s\n", ui.GoldText("TV Shows"), ui.Dim("…")))
	}

	// Requests
	if m.seerr != nil && !m.seerr.Err && len(m.seerr.Requests) > 0 {
		b.WriteString(fmt.Sprintf("\n  %s %s\n", ui.Bold("Requests"), ui.Dim(fmt.Sprintf("(%d)", m.seerr.Total))))
		for _, r := range m.seerr.Requests {
			ti := m.seerr.Titles[r.Media.TmdbID]
			title := ti.Title
			if title == "" {
				title = "…"
			}
			if len(title) > 40 {
				title = title[:40] + "…"
			}
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
			status := statusNames[r.Status]
			s4k := ""
			if r.Is4K {
				s4k = " 4K"
			}
			b.WriteString(fmt.Sprintf("  %s %-12s %s (%s)%s\n", colorFn(icon), colorFn(status), title, ti.Year, s4k))
		}
	}

	// Activity
	if m.commands != nil {
		var active []statusCommandInfo
		for _, c := range m.commands.Commands {
			if c.Status == "started" || c.Status == "queued" {
				active = append(active, c)
			}
		}
		if len(active) > 0 {
			b.WriteString(fmt.Sprintf("\n  %s\n", ui.Bold("Activity")))
			for _, c := range active {
				icon := ui.Warn("⟳")
				if c.Status == "queued" {
					icon = ui.Dim("◷")
				}
				b.WriteString(fmt.Sprintf("  %s %s %s %s\n", icon, ui.Dim("["+c.Svc+"]"), c.Name, ui.Dim(c.Status)))
			}
		}
	}

	// Health
	if m.health != nil && len(m.health.Items) > 0 {
		b.WriteString(fmt.Sprintf("\n  %s\n", ui.Bold("Health")))
		for _, item := range m.health.Items {
			level := ui.Warn("WARN")
			if item.Type == "error" {
				level = ui.Err("ERROR")
			}
			msg := item.Message
			if len(msg) > 58 {
				msg = msg[:58] + "…"
			}
			b.WriteString(fmt.Sprintf("  %s %s %s\n", level, ui.Dim("["+item.Svc+"]"), msg))
		}
	}

	// Queues
	hasQ := (m.radarrQueue != nil && m.radarrQueue.Total > 0) || (m.sonarrQueue != nil && m.sonarrQueue.Total > 0)
	if hasQ {
		b.WriteString(fmt.Sprintf("\n  %s\n", ui.Bold("Queues")))
		for _, q := range []*queueResult{m.radarrQueue, m.sonarrQueue} {
			if q == nil {
				continue
			}
			for _, rec := range q.Records {
				colorFn := ui.Err
				if rec.TrackedDownloadState == "downloading" {
					colorFn = ui.Ok
				} else if rec.TrackedDownloadState == "importPending" {
					colorFn = ui.Warn
				}
				title := rec.Title
				if len(title) > 42 {
					title = title[:42] + "…"
				}
				pct := ""
				if rec.Size > 0 {
					pct = ui.Dim(fmt.Sprintf(" %.0f%%", (1-rec.Sizeleft/rec.Size)*100))
				}
				b.WriteString(fmt.Sprintf("  %s %-14s %s%s\n", ui.Dim("["+q.Svc+"]"), colorFn(rec.TrackedDownloadState), title, pct))
			}
		}
	}

	// Torrents
	if m.torrents != nil && !m.torrents.Err {
		dlStates := map[string]bool{"downloading": true, "stalledDL": true, "forcedDL": true, "metaDL": true}
		seedStates := map[string]bool{"uploading": true, "stalledUP": true, "forcedUP": true}
		var dlCount, seedCount int
		var totalDL int64
		for _, t := range m.torrents.Torrents {
			if dlStates[t.State] {
				dlCount++
				totalDL += t.DLSpeed
			}
			if seedStates[t.State] {
				seedCount++
			}
		}
		b.WriteString(fmt.Sprintf("\n  %s\n", ui.Bold("Torrents")))
		if dlCount > 0 {
			for _, t := range m.torrents.Torrents {
				if !dlStates[t.State] {
					continue
				}
				pct := int(t.Progress * 100)
				speed := float64(t.DLSpeed) / 1048576
				name := t.Name
				if len(name) > 38 {
					name = name[:38] + "…"
				}
				barLen := 12
				filled := barLen * pct / 100
				bar := strings.Repeat("█", filled) + strings.Repeat("░", barLen-filled)
				eta := fmtETA(t.ETA)
				b.WriteString(fmt.Sprintf("  [%s] %s %s  %s %s\n",
					bar, ui.GoldText(fmt.Sprintf("%3d%%", pct)),
					fmt.Sprintf("%.1f MB/s", speed), name, ui.Dim(eta)))
			}
		}
		b.WriteString(fmt.Sprintf("  %s\n", ui.Dim(fmt.Sprintf(
			"%d downloading (%.1f MB/s), %d seeding, %d total",
			dlCount, float64(totalDL)/1048576, seedCount, len(m.torrents.Torrents)))))
	}

	// Disk
	if m.disk != nil && !m.disk.Err {
		used := m.disk.Total - m.disk.Free
		pct := float64(used) / float64(m.disk.Total) * 100
		barLen := 20
		filled := int(float64(barLen) * pct / 100)
		bar := strings.Repeat("█", filled) + strings.Repeat("░", barLen-filled)
		colorFn := ui.Ok
		if pct >= 90 {
			colorFn = ui.Err
		} else if pct >= 80 {
			colorFn = ui.Warn
		}
		b.WriteString(fmt.Sprintf("\n  %s  [%s] %s  %s free / %s\n",
			ui.Bold("Disk"), bar, colorFn(fmt.Sprintf("%.0f%%", pct)),
			ui.FmtSize(m.disk.Free), ui.FmtSize(m.disk.Total)))
	}

	// Footer
	b.WriteString(fmt.Sprintf("\n  %s\n", ui.Dim("r refresh  q quit")))

	return b.String()
}

func renderServiceCell(services map[string]serviceResult, name string) string {
	svc := config.Get().Services[name]
	r, ok := services[name]
	if !ok {
		return fmt.Sprintf("%s %-13s%s %s",
			ui.Dim("◌"), name, ui.Dim(fmt.Sprintf(":%d", svc.Port)), ui.Dim("…"))
	}
	if r.Up {
		return fmt.Sprintf("%s %-13s%s %s",
			ui.Ok("●"), name, ui.Dim(fmt.Sprintf(":%d", svc.Port)),
			ui.Dim(fmt.Sprintf("%dms", r.Ms)))
	}
	return fmt.Sprintf("%s %-13s%s %s",
		ui.Err("○"), name, ui.Dim(fmt.Sprintf(":%d", svc.Port)),
		ui.Err("down"))
}

func runStatusTUI() error {
	// Force lipgloss to use color (alt screen)
	lipgloss.SetHasDarkBackground(true)
	p := tea.NewProgram(newTuiModel(), tea.WithAltScreen())
	_, err := p.Run()
	return err
}
