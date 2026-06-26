package skills

import (
	"github.com/maxtechera/admirarr/internal/qbit"
)

// DownloadItem represents a torrent from qBittorrent.
type DownloadItem struct {
	Hash     string  `json:"hash"`
	Name     string  `json:"name"`
	Size     int64   `json:"size"`
	Progress float64 `json:"progress"`
	DLSpeed  int64   `json:"dl_speed"`
	UPSpeed  int64   `json:"up_speed"`
	State    string  `json:"state"`
	ETA      int64   `json:"eta"`
	Category string  `json:"category"`
}

// ListDownloads fetches all torrents from qBittorrent.
func ListDownloads() ([]DownloadItem, error) {
	data, err := qbit.New().Torrents()
	if err != nil {
		return nil, err
	}

	items := make([]DownloadItem, len(data))
	for i, t := range data {
		items[i] = DownloadItem{
			Hash:     t.Hash,
			Name:     t.Name,
			Size:     t.Size,
			Progress: t.Progress,
			DLSpeed:  t.DLSpeed,
			UPSpeed:  t.UPSpeed,
			State:    t.State,
			ETA:      t.ETA,
			Category: t.Category,
		}
	}
	return items, nil
}
