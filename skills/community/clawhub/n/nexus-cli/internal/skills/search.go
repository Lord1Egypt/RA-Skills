package skills

import (
	"sort"

	"github.com/maxtechera/admirarr/internal/arr"
)

// SearchResultItem represents a Prowlarr search result.
type SearchResultItem struct {
	Title   string `json:"title"`
	Size    int64  `json:"size"`
	Seeders int    `json:"seeders"`
	Indexer string `json:"indexer"`
}

// SearchIndexers searches Prowlarr indexers, returns results sorted by seeders desc.
func SearchIndexers(query string) ([]SearchResultItem, error) {
	data, err := arr.New("prowlarr").Search(query)
	if err != nil {
		return nil, err
	}

	sort.Slice(data, func(i, j int) bool { return data[i].Seeders > data[j].Seeders })

	items := make([]SearchResultItem, len(data))
	for i, r := range data {
		items[i] = SearchResultItem{
			Title:   r.Title,
			Size:    r.Size,
			Seeders: r.Seeders,
			Indexer: r.Indexer,
		}
	}
	return items, nil
}
