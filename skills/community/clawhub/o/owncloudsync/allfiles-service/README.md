## Prerequisites on OwnCloud Server
- OwnCloud lacks a satisfactory built-in file search service, so an indexing service is required.
- A small script must be configured then installed with crontab (run daily): findallfiles.sh
- A Go program (`allfiles-service.go`) is provided to serve the result of the above script
- Compile the Go program with:
  ```
  go build -ldflags="-s -w" -o /usr/local/bin/allfiles-service allfiles-service.go
  ```
- Configure credentials (`ALLFILES_USER`, `ALLFILES_PASS`) in the service definition (`allfiles.service`) to match the ones in the owncloud.json file.
- Install and enable the provided systemd service `allfiles.service`.
- Place valid certificates (default location: `/etc/allfiles/certs/`).
