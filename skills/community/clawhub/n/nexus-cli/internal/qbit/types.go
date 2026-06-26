package qbit

// Torrent represents a qBittorrent torrent entry.
type Torrent struct {
	Hash     string  `json:"hash"`
	Name     string  `json:"name"`
	Size     int64   `json:"size"`
	Progress float64 `json:"progress"`
	DLSpeed  int64   `json:"dlspeed"`
	UPSpeed  int64   `json:"upspeed"`
	State    string  `json:"state"`
	ETA      int64   `json:"eta"`
	Category string  `json:"category"`
	SavePath string  `json:"save_path"`
}

// Preferences holds qBittorrent application preferences.
type Preferences struct {
	SavePath      string `json:"save_path"`
	WebUIAddress  string `json:"web_ui_address"`
	WebUIPort     int    `json:"web_ui_port"`
	WebUIUsername string `json:"web_ui_username"`
	ListenPort    int    `json:"listen_port"`
	DHTIP         bool   `json:"dht"`
	MaxConnec     int    `json:"max_connec"`
	MaxUploads    int    `json:"max_uploads"`
	DLLimit       int    `json:"dl_limit"`
	UPLimit       int    `json:"up_limit"`
	Locale        string `json:"locale"`
}

// Category represents a qBittorrent torrent category.
type Category struct {
	Name     string `json:"name"`
	SavePath string `json:"savePath"`
}
