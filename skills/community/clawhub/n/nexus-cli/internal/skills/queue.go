package skills

import (
	"github.com/maxtechera/admirarr/internal/arr"
)

// QueueItem represents a single item in an import queue.
type QueueItem struct {
	Title    string   `json:"title"`
	State    string   `json:"state"`
	Size     float64  `json:"size"`
	Sizeleft float64  `json:"sizeleft"`
	Warnings []string `json:"warnings,omitempty"`
}

// QueueResult holds the queue for a single service.
type QueueResult struct {
	Service string      `json:"service"`
	Total   int         `json:"total"`
	Items   []QueueItem `json:"items"`
}

// ListQueues fetches import queues from Radarr and Sonarr.
func ListQueues() ([]QueueResult, error) {
	var results []QueueResult

	for _, svc := range []string{"radarr", "sonarr"} {
		page, err := arr.New(svc).Queue(50)
		if err != nil {
			results = append(results, QueueResult{
				Service: svc,
				Total:   0,
				Items:   []QueueItem{},
			})
			continue
		}

		items := make([]QueueItem, len(page.Records))
		for i, rec := range page.Records {
			var warnings []string
			for _, sm := range rec.StatusMessages {
				warnings = append(warnings, sm.Messages...)
			}
			items[i] = QueueItem{
				Title:    rec.Title,
				State:    rec.TrackedDownloadState,
				Size:     rec.Size,
				Sizeleft: rec.Sizeleft,
				Warnings: warnings,
			}
		}

		results = append(results, QueueResult{
			Service: svc,
			Total:   page.TotalRecords,
			Items:   items,
		})
	}

	return results, nil
}
