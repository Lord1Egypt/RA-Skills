package arr

// Movie represents a Radarr movie.
type Movie struct {
	ID               int    `json:"id"`
	TmdbID           int    `json:"tmdbId"`
	Title            string `json:"title"`
	Year             int    `json:"year"`
	HasFile          bool   `json:"hasFile"`
	Monitored        bool   `json:"monitored"`
	SizeOnDisk       int64  `json:"sizeOnDisk"`
	Status           string `json:"status"`
	QualityProfileID int    `json:"qualityProfileId"`
}

// Series represents a Sonarr series.
type Series struct {
	ID               int         `json:"id"`
	TvdbID           int         `json:"tvdbId"`
	Title            string      `json:"title"`
	Year             int         `json:"year"`
	Monitored        bool        `json:"monitored"`
	QualityProfileID int         `json:"qualityProfileId"`
	Statistics       SeriesStats `json:"statistics"`
}

// SeriesStats holds episode statistics for a series.
type SeriesStats struct {
	EpisodeCount     int   `json:"episodeCount"`
	EpisodeFileCount int   `json:"episodeFileCount"`
	SizeOnDisk       int64 `json:"sizeOnDisk"`
}

// QueuePage represents a paginated queue response.
type QueuePage struct {
	TotalRecords int           `json:"totalRecords"`
	Records      []QueueRecord `json:"records"`
}

// QueueRecord represents a single queue entry.
type QueueRecord struct {
	Title                string          `json:"title"`
	TrackedDownloadState string          `json:"trackedDownloadState"`
	Sizeleft             float64         `json:"sizeleft"`
	Size                 float64         `json:"size"`
	StatusMessages       []StatusMessage `json:"statusMessages"`
}

// StatusMessage represents a queue item warning.
type StatusMessage struct {
	Messages []string `json:"messages"`
}

// RootFolder represents a root folder entry.
type RootFolder struct {
	ID         int    `json:"id"`
	Path       string `json:"path"`
	Accessible bool   `json:"accessible"`
	FreeSpace  int64  `json:"freeSpace"`
}

// QualityProfile represents a quality profile.
type QualityProfile struct {
	ID   int    `json:"id"`
	Name string `json:"name"`
}

// CustomFormat represents a Radarr/Sonarr custom format.
type CustomFormat struct {
	ID   int    `json:"id"`
	Name string `json:"name"`
}

// HealthItem represents a health check warning.
type HealthItem struct {
	Type    string `json:"type"`
	Message string `json:"message"`
	WikiURL string `json:"wikiUrl"`
	Source  string `json:"source"`
}

// Command represents an active *Arr command/task.
type Command struct {
	Name   string `json:"name"`
	Status string `json:"status"`
}

// SearchResult represents a Prowlarr search result.
type SearchResult struct {
	Title   string `json:"title"`
	Size    int64  `json:"size"`
	Seeders int    `json:"seeders"`
	Indexer string `json:"indexer"`
}

// Indexer represents a Prowlarr indexer.
type Indexer struct {
	ID             int                      `json:"id"`
	Name           string                   `json:"name"`
	Enable         bool                     `json:"enable"`
	Implementation string                   `json:"implementation"`
	ConfigContract string                   `json:"configContract"`
	Protocol       string                   `json:"protocol"`
	Tags           []int                    `json:"tags"`
	Fields         []map[string]interface{} `json:"fields,omitempty"`
	Capabilities   struct {
		Categories []struct {
			Name string `json:"name"`
		} `json:"categories"`
	} `json:"capabilities"`
}

// IndexerStatus represents a Prowlarr indexer status entry.
type IndexerStatus struct {
	IndexerID         int    `json:"indexerId"`
	MostRecentFailure string `json:"mostRecentFailure"`
	DisabledTill      string `json:"disabledTill"`
}

// IndexerTestResult represents a Prowlarr indexer test result.
type IndexerTestResult struct {
	ID                 int  `json:"id"`
	IsValid            bool `json:"isValid"`
	ValidationFailures []struct {
		ErrorMessage string `json:"errorMessage"`
	} `json:"validationFailures"`
}

// WantedMissingPage represents a paginated wanted/missing response.
type WantedMissingPage struct {
	TotalRecords int              `json:"totalRecords"`
	Records      []MissingEpisode `json:"records"`
}

// MissingEpisode represents a missing episode from Sonarr.
type MissingEpisode struct {
	Title         string `json:"title"`
	SeasonNumber  int    `json:"seasonNumber"`
	EpisodeNumber int    `json:"episodeNumber"`
	Series        struct {
		Title string `json:"title"`
	} `json:"series"`
}

// DownloadClient represents a *Arr download client entry.
type DownloadClient struct {
	ID                       int                   `json:"id"`
	Name                     string                `json:"name"`
	Enable                   bool                  `json:"enable"`
	Implementation           string                `json:"implementation"`
	ConfigContract           string                `json:"configContract"`
	Fields                   []DownloadClientField `json:"fields"`
	Protocol                 string                `json:"protocol"`
	Priority                 int                   `json:"priority"`
	Tags                     []int                 `json:"tags"`
	RemoveCompletedDownloads bool                  `json:"removeCompletedDownloads"`
	RemoveFailedDownloads    bool                  `json:"removeFailedDownloads"`
}

// DownloadClientField represents a field in a download client config.
type DownloadClientField struct {
	Name  string      `json:"name"`
	Value interface{} `json:"value"`
}

// GetField returns the value of a named field.
func (dc *DownloadClient) GetField(name string) interface{} {
	for _, f := range dc.Fields {
		if f.Name == name {
			return f.Value
		}
	}
	return nil
}

// SetField sets the value of a named field, creating it if necessary.
func (dc *DownloadClient) SetField(name string, value interface{}) {
	for i, f := range dc.Fields {
		if f.Name == name {
			dc.Fields[i].Value = value
			return
		}
	}
	dc.Fields = append(dc.Fields, DownloadClientField{Name: name, Value: value})
}

// Release represents a Radarr release search result.
type Release struct {
	Title      string   `json:"title"`
	Size       int64    `json:"size"`
	Seeders    int      `json:"seeders"`
	Rejected   bool     `json:"rejected"`
	Quality    struct {
		Quality struct {
			Name string `json:"name"`
		} `json:"quality"`
	} `json:"quality"`
	Rejections []string `json:"rejections"`
}
