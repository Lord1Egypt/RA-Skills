package ui

import "testing"

func TestFmtSize(t *testing.T) {
	tests := []struct {
		bytes    int64
		expected string
	}{
		{0, "0 GB"},
		{1073741824, "1.00 GB"},               // 1 GB
		{536870912, "0.50 GB"},                 // 0.5 GB
		{1099511627776, "1.00 TB"},             // 1 TB
		{2199023255552, "2.00 TB"},             // 2 TB
		{5368709120, "5.00 GB"},                // 5 GB
		{107374182400, "100.00 GB"},            // 100 GB
	}
	for _, tt := range tests {
		got := FmtSize(tt.bytes)
		if got != tt.expected {
			t.Errorf("FmtSize(%d) = %q, want %q", tt.bytes, got, tt.expected)
		}
	}
}

func TestSeparator_NotEmpty(t *testing.T) {
	sep := Separator()
	if sep == "" {
		t.Error("separator should not be empty")
	}
}

func TestFormatFunctions_NotEmpty(t *testing.T) {
	// Verify formatting functions return non-empty strings
	fns := []struct {
		name string
		fn   func(string) string
	}{
		{"Ok", Ok},
		{"Err", Err},
		{"Warn", Warn},
		{"Bold", Bold},
		{"Dim", Dim},
		{"CyanText", CyanText},
		{"GoldText", GoldText},
	}
	for _, tt := range fns {
		t.Run(tt.name, func(t *testing.T) {
			result := tt.fn("test")
			if result == "" {
				t.Errorf("%s returned empty string", tt.name)
			}
			// In a non-TTY test environment, lipgloss may or may not apply styles,
			// but the text content should be preserved
			if len(result) < 4 { // "test" = 4 chars minimum
				t.Errorf("%s result too short: %q", tt.name, result)
			}
		})
	}
}
