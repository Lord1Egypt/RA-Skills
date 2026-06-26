package skills

import (
	"fmt"
	"sort"
	"strings"

	"github.com/maxtechera/admirarr/internal/arr"
)

// MovieItem represents a movie from Radarr.
type MovieItem struct {
	ID         int    `json:"id"`
	Title      string `json:"title"`
	Year       int    `json:"year"`
	HasFile    bool   `json:"has_file"`
	SizeOnDisk int64  `json:"size_on_disk"`
	Monitored  bool   `json:"monitored"`
	Status     string `json:"status"`
}

// ListMovies fetches all movies from Radarr, sorted by title.
func ListMovies() ([]MovieItem, error) {
	data, err := arr.New("radarr").Movies()
	if err != nil {
		return nil, err
	}

	sort.Slice(data, func(i, j int) bool { return data[i].Title < data[j].Title })

	items := make([]MovieItem, len(data))
	for i, m := range data {
		items[i] = MovieItem{
			ID:         m.ID,
			Title:      m.Title,
			Year:       m.Year,
			HasFile:    m.HasFile,
			SizeOnDisk: m.SizeOnDisk,
			Monitored:  m.Monitored,
			Status:     m.Status,
		}
	}
	return items, nil
}

// ReleaseItem represents a single release result from Radarr.
type ReleaseItem struct {
	Title      string   `json:"title"`
	Quality    string   `json:"quality"`
	Size       int64    `json:"size"`
	Seeders    int      `json:"seeders"`
	Rejected   bool     `json:"rejected"`
	Rejections []string `json:"rejections,omitempty"`
}

// FindResult holds the movie and its available releases.
type FindResult struct {
	Movie    MovieItem     `json:"movie"`
	Releases []ReleaseItem `json:"releases"`
}

// FindReleases finds a movie by title substring and fetches its releases.
func FindReleases(query string) (*FindResult, error) {
	query = strings.ToLower(query)
	client := arr.New("radarr")

	movies, err := client.Movies()
	if err != nil {
		return nil, err
	}

	var match *arr.Movie
	for i, m := range movies {
		if strings.Contains(strings.ToLower(m.Title), query) {
			match = &movies[i]
			break
		}
	}
	if match == nil {
		return nil, fmt.Errorf("movie not found in Radarr: %s", query)
	}

	releases, err := client.Releases(match.ID)
	if err != nil {
		return nil, err
	}

	result := &FindResult{
		Movie: MovieItem{
			ID:         match.ID,
			Title:      match.Title,
			Year:       match.Year,
			HasFile:    match.HasFile,
			SizeOnDisk: match.SizeOnDisk,
			Monitored:  match.Monitored,
			Status:     match.Status,
		},
		Releases: make([]ReleaseItem, len(releases)),
	}
	for i, r := range releases {
		result.Releases[i] = ReleaseItem{
			Title:      r.Title,
			Quality:    r.Quality.Quality.Name,
			Size:       r.Size,
			Seeders:    r.Seeders,
			Rejected:   r.Rejected,
			Rejections: r.Rejections,
		}
	}
	return result, nil
}

// LookupMovies searches Radarr for movies matching a query (for add-movie).
func LookupMovies(query string) ([]map[string]interface{}, error) {
	return arr.New("radarr").LookupMovie(query)
}

// AddMovie adds a movie to Radarr with the given profile and root folder.
func AddMovie(movie map[string]interface{}, profileID int, rootFolder string) (map[string]interface{}, error) {
	movie["qualityProfileId"] = profileID
	movie["rootFolderPath"] = rootFolder
	movie["monitored"] = true
	movie["addOptions"] = map[string]bool{"searchForMovie": true}
	return arr.New("radarr").AddMovie(movie)
}
