package gwt

import (
	"strings"
	"testing"
)

func TestBuildRetrieveItineraryBody(t *testing.T) {
	const remoteHost = "www.lynx-reservations.com"
	const fileIdentifier = "$43q"

	tests := []struct {
		name          string
		showCancelled bool
		wantContains  string
	}{
		{
			name:          "excludes cancelled by default",
			showCancelled: false,
			wantContains:  fileIdentifier + "|0|0|0|",
		},
		{
			name:          "includes cancelled when flag is set",
			showCancelled: true,
			wantContains:  fileIdentifier + "|1|0|0|",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			body := BuildRetrieveItineraryBody(remoteHost, fileIdentifier, tt.showCancelled)

			if !strings.Contains(body, tt.wantContains) {
				t.Errorf("BuildRetrieveItineraryBody(%q, %v)\ngot:  %s\nwant substring: %s",
					fileIdentifier, tt.showCancelled, body, tt.wantContains)
			}

			// Verify remote host is embedded correctly
			if !strings.Contains(body, "https://"+remoteHost+"/lynx/lynx/") {
				t.Errorf("expected body to contain host URL, got: %s", body)
			}

			// Verify the correct RPC method is targeted
			if !strings.Contains(body, "retrieveItinerary") {
				t.Errorf("expected body to contain 'retrieveItinerary', got: %s", body)
			}
		})
	}
}
