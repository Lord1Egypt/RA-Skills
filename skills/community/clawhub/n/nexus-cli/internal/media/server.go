package media

// MediaServer is the interface for media server operations.
type MediaServer interface {
	Name() string
	RecentlyAdded(limit int) ([]MediaItem, error)
	LibraryScan() ([]ScanResult, error)
	WatchHistory(limit int) ([]WatchEntry, error)
}

// MediaItem represents a recently added piece of content.
type MediaItem struct {
	Title string
	Year  string
	Type  string // "movie", "episode", "show"
}

// ScanResult represents the outcome of a library scan.
type ScanResult struct {
	Library string
	OK      bool
	Err     error
}

// WatchEntry represents a single watch history entry.
type WatchEntry struct {
	Title   string
	User    string
	Minutes int
}
