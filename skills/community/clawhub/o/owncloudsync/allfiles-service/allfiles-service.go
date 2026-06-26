package main

import (
	"crypto/subtle"
	"io"
	"log"
	"net/http"
	"os"
)

var (
	username = os.Getenv("ALLFILES_USER")
	password = os.Getenv("ALLFILES_PASS")
	listen   = ":8443" // change to ":443" if you want standard port
	cert     = "/etc/allfiles/certs/fullchain.pem"
	key      = "/etc/allfiles/certs/privkey.pem"
)

func basicAuth(next http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		user, pass, ok := r.BasicAuth()
		if !ok || subtle.ConstantTimeCompare([]byte(user), []byte(username)) != 1 ||
			subtle.ConstantTimeCompare([]byte(pass), []byte(password)) != 1 {
			w.Header().Set("WWW-Authenticate", `Basic realm="allfiles"`)
			http.Error(w, "Unauthorized", http.StatusUnauthorized)
			return
		}
		next(w, r)
	}
}

func allfilesHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	// ---------------------------------------------------------------------------
	// Guard against symlink attacks: reject any attempt to serve /tmp/allfiles.txt
	// if it has been replaced by a symbolic link. A local attacker could otherwise
	// point it to an arbitrary file (e.g. /etc/passwd) and leak its contents
	// through the /allfiles endpoint.
	// ---------------------------------------------------------------------------
	info, err := os.Lstat("/tmp/allfiles.txt")
	if err != nil {
		http.Error(w, "File not found", http.StatusNotFound)
		return
	}
	if info.Mode()&os.ModeSymlink != 0 {
		log.Println("SECURITY: /tmp/allfiles.txt is a symbolic link — possible symlink attack detected.")
		http.Error(w, "Internal server error", http.StatusInternalServerError)
		return
	}

	f, err := os.Open("/tmp/allfiles.txt")
	if err != nil {
		http.Error(w, "File not found", http.StatusNotFound)
		return
	}
	defer f.Close()

	w.Header().Set("Content-Type", "text/plain; charset=utf-8")
	w.Header().Set("Cache-Control", "no-cache, no-store")
	io.Copy(w, f)
}

func main() {
	if username == "" || password == "" {
		log.Fatal("Environnement variables BASIC_USER and BASIC_PASS are mandatory")
	}

	http.HandleFunc("/allfiles", basicAuth(allfilesHandler))

	log.Printf("✅ Service started", listen)
	log.Fatal(http.ListenAndServeTLS(listen, cert, key, nil))
}
