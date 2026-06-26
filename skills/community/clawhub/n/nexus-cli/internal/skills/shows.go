package skills

import (
	"sort"

	"github.com/maxtechera/admirarr/internal/arr"
)

// ShowItem represents a TV show from Sonarr.
type ShowItem struct {
	ID           int    `json:"id"`
	Title        string `json:"title"`
	Year         int    `json:"year"`
	Episodes     int    `json:"episodes"`
	EpisodeFiles int    `json:"episode_files"`
	SizeOnDisk   int64  `json:"size_on_disk"`
	Monitored    bool   `json:"monitored"`
}

// ListShows fetches all shows from Sonarr, sorted by title.
func ListShows() ([]ShowItem, error) {
	data, err := arr.New("sonarr").Series()
	if err != nil {
		return nil, err
	}

	sort.Slice(data, func(i, j int) bool { return data[i].Title < data[j].Title })

	items := make([]ShowItem, len(data))
	for i, s := range data {
		items[i] = ShowItem{
			ID:           s.ID,
			Title:        s.Title,
			Year:         s.Year,
			Episodes:     s.Statistics.EpisodeCount,
			EpisodeFiles: s.Statistics.EpisodeFileCount,
			SizeOnDisk:   s.Statistics.SizeOnDisk,
			Monitored:    s.Monitored,
		}
	}
	return items, nil
}

// LookupShows searches Sonarr for series matching a query.
func LookupShows(query string) ([]map[string]interface{}, error) {
	return arr.New("sonarr").LookupSeries(query)
}

// AddShow adds a show to Sonarr with the given profile and root folder.
func AddShow(series map[string]interface{}, profileID int, rootFolder string) (map[string]interface{}, error) {
	series["qualityProfileId"] = profileID
	series["rootFolderPath"] = rootFolder
	series["monitored"] = true
	series["addOptions"] = map[string]interface{}{
		"searchForMissingEpisodes": true,
		"monitor":                  "all",
	}
	return arr.New("sonarr").AddSeries(series)
}
