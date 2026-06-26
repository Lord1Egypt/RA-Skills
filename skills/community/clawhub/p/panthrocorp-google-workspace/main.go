package main

import (
	"os"
	"runtime/debug"

	"github.com/PanthroCorp-Limited/openclaw-skills/google-workspace/cmd"
)

// version is overridden at build time by GoReleaser via -X main.version=...
var version = "dev"

func getVersion() string {
	// For `go install module@vX.Y.Z` the module version is embedded in build info.
	if info, ok := debug.ReadBuildInfo(); ok &&
		info.Main.Version != "" &&
		info.Main.Version != "(devel)" {
		return info.Main.Version
	}
	return version
}

func main() {
	version := getVersion()
	cmd.SetVersion(version)
	if err := cmd.Execute(); err != nil {
		os.Exit(1)
	}
}
