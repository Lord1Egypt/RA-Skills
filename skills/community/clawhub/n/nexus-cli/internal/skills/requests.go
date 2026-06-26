package skills

import (
	"fmt"

	"github.com/maxtechera/admirarr/internal/seerr"
)

// RequestItem represents a resolved Seerr media request.
type RequestItem struct {
	Title  string `json:"title"`
	Year   string `json:"year"`
	Status string `json:"status"`
	User   string `json:"user"`
	Is4K   bool   `json:"is_4k"`
	Type   string `json:"type"`
}

// StatusNames maps Seerr status codes to human-readable names.
var StatusNames = map[int]string{
	1: "PENDING",
	2: "APPROVED",
	3: "DECLINED",
	4: "AVAILABLE",
	5: "PROCESSING",
}

// ListRequests fetches and resolves media requests from Seerr.
// Returns items, total count, and error.
func ListRequests(limit int) ([]RequestItem, int, error) {
	client := seerr.New()
	data, err := client.Requests(limit)
	if err != nil {
		return nil, 0, err
	}

	items := make([]RequestItem, len(data.Results))
	for i, r := range data.Results {
		title, year := client.ResolveTitle(r.Media.MediaType, r.Media.TmdbID)
		status := StatusNames[r.Status]
		if status == "" {
			status = fmt.Sprintf("?(%d)", r.Status)
		}
		items[i] = RequestItem{
			Title:  title,
			Year:   year,
			Status: status,
			User:   r.RequestedBy.DisplayName,
			Is4K:   r.Is4K,
			Type:   r.Media.MediaType,
		}
	}

	return items, data.PageInfo.Results, nil
}
