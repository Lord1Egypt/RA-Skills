package cmd

import (
	"fmt"

	"github.com/maxtechera/admirarr/internal/arr"
	"github.com/maxtechera/admirarr/internal/ui"
	"github.com/spf13/cobra"
)

var queueCmd = &cobra.Command{
	Use:   "queue",
	Short: "Radarr + Sonarr import queues",
	Long: `Show Radarr and Sonarr import queues.

Displays items waiting to be imported with title, status, and warnings.

API endpoints used:
  Radarr   GET /api/v3/queue?pageSize=50
  Sonarr   GET /api/v3/queue?pageSize=50`,
	Example: "  admirarr queue",
	Run:     runQueue,
}

func init() {
	rootCmd.AddCommand(queueCmd)
}

func runQueue(cmd *cobra.Command, args []string) {
	type queueItemOut struct {
		Title string `json:"title"`
		State string `json:"state"`
	}
	type queueOut struct {
		Radarr []queueItemOut `json:"radarr"`
		Sonarr []queueItemOut `json:"sonarr"`
	}

	jsonOut := queueOut{
		Radarr: []queueItemOut{},
		Sonarr: []queueItemOut{},
	}

	type svcData struct {
		svc   string
		total int
		page  *arr.QueuePage
	}
	var allData []svcData

	for _, svc := range []string{"radarr", "sonarr"} {
		page, err := arr.New(svc).Queue(50)
		total := 0
		if err == nil {
			total = page.TotalRecords
		} else {
			page = &arr.QueuePage{}
		}
		allData = append(allData, svcData{svc: svc, total: total, page: page})
		for _, rec := range page.Records {
			item := queueItemOut{Title: rec.Title, State: rec.TrackedDownloadState}
			if svc == "radarr" {
				jsonOut.Radarr = append(jsonOut.Radarr, item)
			} else {
				jsonOut.Sonarr = append(jsonOut.Sonarr, item)
			}
		}
	}

	ui.PrintOrJSON(jsonOut, func() {
		ui.PrintBanner()
		fmt.Println(ui.Bold("\n  Download Queues\n"))
		for _, sd := range allData {
			svcTitle := sd.svc
			if len(svcTitle) > 0 {
				svcTitle = string(sd.svc[0]-32) + sd.svc[1:]
			}
			fmt.Println(ui.Bold(fmt.Sprintf("  %s (%d items)", svcTitle, sd.total)))
			if sd.total > 0 {
				for _, rec := range sd.page.Records {
					state := rec.TrackedDownloadState
					colorFn := ui.Err
					if state == "downloading" {
						colorFn = ui.Ok
					} else if state == "importPending" {
						colorFn = ui.Warn
					}
					title := rec.Title
					if len(title) > 70 {
						title = title[:70]
					}
					fmt.Printf("    %s  %s\n", colorFn(state), title)
					for _, sm := range rec.StatusMessages {
						for i, m := range sm.Messages {
							if i >= 2 {
								break
							}
							msg := m
							if len(msg) > 80 {
								msg = msg[:80]
							}
							fmt.Printf("      %s\n", ui.Dim(msg))
						}
					}
				}
			} else {
				fmt.Printf("    %s\n", ui.Dim("Empty"))
			}
			fmt.Println()
		}
	})
}
