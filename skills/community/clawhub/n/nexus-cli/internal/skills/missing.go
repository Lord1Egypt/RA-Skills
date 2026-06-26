package skills

import (
	"github.com/maxtechera/admirarr/internal/arr"
)

// MissingMovie represents a monitored movie without a file.
type MissingMovie struct {
	Title  string `json:"title"`
	Year   int    `json:"year"`
	Status string `json:"status"`
}

// MissingEpisode represents a missing episode from Sonarr.
type MissingEpisode struct {
	Series  string `json:"series"`
	Season  int    `json:"season"`
	Episode int    `json:"episode"`
	Title   string `json:"title"`
}

// MissingResult holds missing content from both Radarr and Sonarr.
type MissingResult struct {
	Movies       []MissingMovie   `json:"movies"`
	Episodes     []MissingEpisode `json:"episodes"`
	TotalMissing int              `json:"total_missing_episodes"`
	MoviesErr    error            `json:"-"`
	EpisodesErr  error            `json:"-"`
}

// ListMissing fetches missing content from Radarr and Sonarr.
func ListMissing() *MissingResult {
	result := &MissingResult{
		Movies:   []MissingMovie{},
		Episodes: []MissingEpisode{},
	}

	// Movies from Radarr
	movies, moviesErr := arr.New("radarr").Movies()
	result.MoviesErr = moviesErr
	if moviesErr == nil {
		for _, m := range movies {
			if m.Monitored && !m.HasFile {
				result.Movies = append(result.Movies, MissingMovie{
					Title:  m.Title,
					Year:   m.Year,
					Status: m.Status,
				})
			}
		}
	}

	// Episodes from Sonarr
	eps, epsErr := arr.New("sonarr").WantedMissing(20, map[string]string{
		"sortKey":       "airDateUtc",
		"sortDirection": "descending",
	})
	result.EpisodesErr = epsErr
	if epsErr == nil {
		result.TotalMissing = eps.TotalRecords
		for _, e := range eps.Records {
			result.Episodes = append(result.Episodes, MissingEpisode{
				Series:  e.Series.Title,
				Season:  e.SeasonNumber,
				Episode: e.EpisodeNumber,
				Title:   e.Title,
			})
		}
	}

	return result
}
