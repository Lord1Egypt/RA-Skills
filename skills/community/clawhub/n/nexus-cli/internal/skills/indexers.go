package skills

import (
	"fmt"

	"github.com/maxtechera/admirarr/internal/arr"
)

// IndexerItem represents a Prowlarr indexer with status.
type IndexerItem struct {
	ID      int    `json:"id"`
	Name    string `json:"name"`
	Enabled bool   `json:"enabled"`
	Status  string `json:"status"` // "ok", "disabled", "failing"
}

// IndexerTestItem represents the result of testing a single indexer.
type IndexerTestItem struct {
	ID    int    `json:"id"`
	Name  string `json:"name"`
	Valid bool   `json:"valid"`
	Error string `json:"error,omitempty"`
}

// ListIndexers fetches all indexers with their status.
func ListIndexers() ([]IndexerItem, error) {
	client := arr.New("prowlarr")

	indexers, err := client.Indexers()
	if err != nil {
		return nil, err
	}

	statuses, _ := client.IndexerStatuses()
	failedIDs := make(map[int]bool)
	for _, s := range statuses {
		if s.MostRecentFailure != "" {
			failedIDs[s.IndexerID] = true
		}
	}

	items := make([]IndexerItem, len(indexers))
	for i, idx := range indexers {
		st := "ok"
		if !idx.Enable {
			st = "disabled"
		} else if failedIDs[idx.ID] {
			st = "failing"
		}
		items[i] = IndexerItem{
			ID:      idx.ID,
			Name:    idx.Name,
			Enabled: idx.Enable,
			Status:  st,
		}
	}
	return items, nil
}

// TestIndexers tests all indexer connectivity.
func TestIndexers() ([]IndexerTestItem, error) {
	client := arr.New("prowlarr")

	results, err := client.TestAllIndexers()
	if err != nil {
		return nil, err
	}

	// Get indexer names for the results
	indexers, _ := client.Indexers()
	nameMap := make(map[int]string)
	for _, idx := range indexers {
		nameMap[idx.ID] = idx.Name
	}

	items := make([]IndexerTestItem, len(results))
	for i, r := range results {
		name := nameMap[r.ID]
		if name == "" {
			name = fmt.Sprintf("id=%d", r.ID)
		}
		errMsg := ""
		if !r.IsValid && len(r.ValidationFailures) > 0 {
			errMsg = r.ValidationFailures[0].ErrorMessage
		}
		items[i] = IndexerTestItem{
			ID:    r.ID,
			Name:  name,
			Valid: r.IsValid,
			Error: errMsg,
		}
	}
	return items, nil
}
