package media

import "github.com/maxtechera/admirarr/internal/api"

// Detect returns the running media server, preferring Jellyfin.
func Detect() MediaServer {
	if api.CheckReachable("jellyfin") {
		return &JellyfinServer{}
	}
	if api.CheckReachable("plex") {
		return &PlexServer{}
	}
	return nil
}
