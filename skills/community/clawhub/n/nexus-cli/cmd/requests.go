package cmd

import (
	"fmt"

	"github.com/maxtechera/admirarr/internal/seerr"
	"github.com/maxtechera/admirarr/internal/ui"
	"github.com/spf13/cobra"
)

var requestsCmd = &cobra.Command{
	Use:   "requests",
	Short: "Seerr media requests",
	Long: `Show pending and recent media requests from Seerr.

Fetches all requests and resolves titles via the Seerr media API.

Status: PENDING (awaiting approval), APPROVED (searching/downloading),
AVAILABLE (on disk), DECLINED, PROCESSING.

API endpoints used:
  Seerr   GET /api/v1/request?take=20
  Seerr   GET /api/v1/movie/<tmdbId>  or  /api/v1/tv/<tmdbId>`,
	Example: "  admirarr requests",
	Run:     runRequests,
}

func init() {
	rootCmd.AddCommand(requestsCmd)
}

var statusNames = map[int]string{
	1: "PENDING",
	2: "APPROVED",
	3: "DECLINED",
	4: "AVAILABLE",
	5: "PROCESSING",
}

func runRequests(cmd *cobra.Command, args []string) {
	client := seerr.New()
	data, err := client.Requests(20)
	if err != nil {
		if ui.IsJSON() {
			ui.PrintJSON(map[string]string{"error": "Cannot reach Seerr"})
		} else {
			ui.PrintBanner()
			fmt.Printf("\n  %s\n\n", ui.Err("Cannot reach Seerr"))
		}
		return
	}

	type requestOut struct {
		Title  string `json:"title"`
		Year   string `json:"year"`
		Status string `json:"status"`
		User   string `json:"user"`
		Is4K   bool   `json:"is_4k"`
	}
	var out []requestOut
	for _, r := range data.Results {
		title, year := client.ResolveTitle(r.Media.MediaType, r.Media.TmdbID)
		status := statusNames[r.Status]
		if status == "" {
			status = fmt.Sprintf("?(%d)", r.Status)
		}
		out = append(out, requestOut{Title: title, Year: year, Status: status, User: r.RequestedBy.DisplayName, Is4K: r.Is4K})
	}

	ui.PrintOrJSON(out, func() {
		ui.PrintBanner()
		fmt.Printf("%s\n", ui.Bold(fmt.Sprintf("\n  Seerr — Requests (%d total)\n", data.PageInfo.Results)))

		if len(data.Results) == 0 {
			fmt.Printf("  %s\n\n", ui.Dim("No requests"))
			return
		}

		for i, r := range data.Results {
			icon := "○"
			colorFn := ui.Dim
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
			case 3:
				icon = "✗"
				colorFn = ui.Err
			}

			suffix := ""
			if r.Is4K {
				suffix = " [4K]"
			}
			user := r.RequestedBy.DisplayName
			date := r.CreatedAt
			if len(date) > 10 {
				date = date[:10]
			}

			fmt.Printf("  %s %-12s %s (%s)%s  — %s, %s\n",
				colorFn(icon), colorFn(out[i].Status), out[i].Title, out[i].Year, suffix, ui.Dim(user), ui.Dim(date))
		}
		fmt.Println()
	})
}

// resolveTitle is kept for use by status.go which calls it directly.
func resolveTitle(mediaType string, tmdbID int) (string, string) {
	return seerr.New().ResolveTitle(mediaType, tmdbID)
}
