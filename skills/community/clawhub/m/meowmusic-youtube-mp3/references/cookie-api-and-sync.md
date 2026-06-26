# Cookie API and Windows Sync

Use this when you need Windows Chrome cookies on the server for YouTube download reliability.

## Expected server endpoints

Recommended endpoints:

- `GET /api/admin/youtube-cookie/status`
- `POST /api/admin/youtube-cookie/update`

Minimal Go handler pattern:

```go
func youtubeCookiePath() string {
    return filepath.Join(".", "youtube-cookies.txt")
}

func HandleYouTubeCookieStatus(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(map[string]interface{}{
        "status": "success",
        "cookie": youtubeCookieStatus(),
    })
}

func HandleYouTubeCookieUpdate(w http.ResponseWriter, r *http.Request) {
    if r.Method != http.MethodPost {
        http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
        return
    }

    var req struct { Content string `json:"content"` }
    body, _ := io.ReadAll(r.Body)
    if err := json.Unmarshal(body, &req); err != nil {
        http.Error(w, "Invalid JSON", http.StatusBadRequest)
        return
    }

    content := strings.TrimSpace(req.Content)
    if content == "" || !strings.Contains(content, "youtube.com") || !strings.Contains(content, "Netscape HTTP Cookie File") {
        http.Error(w, "Invalid YouTube cookie file", http.StatusBadRequest)
        return
    }

    path := youtubeCookiePath()
    tmpPath := path + ".tmp"
    os.WriteFile(tmpPath, []byte(content+"\n"), 0600)
    os.Rename(tmpPath, path)

    json.NewEncoder(w).Encode(map[string]interface{}{"status": "success"})
}
```

## Windows-side sync pattern

Use `scripts/youtube_cookie_sync.py`.

Behavior:
1. Export cookies from Chrome/Edge/Firefox with `yt-dlp --cookies-from-browser`.
2. Tolerate a local validation failure if the cookie file was still successfully exported.
3. POST cookie text to the server API.

## Security notes

- Never hardcode production bearer tokens inside the published skill.
- Keep the Windows wrapper generic and rely on env vars:
  - `MEOW_SERVER_URL`
  - `MEOW_BEARER_TOKEN`
- Write cookie files atomically on the server (`.tmp` then rename).
