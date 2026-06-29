package cli

import (
	"os"
	"path/filepath"
	"regexp"
	"strings"
	"testing"
)

// realisticIdentifierPatterns are the shapes a ClawHub "Natural-Language Policy
// Violation" flags in fixtures/goldens: a Google Health resource name carrying a
// persistent *numeric user id*, or a long opaque numeric record id that reads as
// real production data. Committed test data must be unmistakably synthetic — the
// `users/me` alias and short placeholder ids — so the repo cannot leak a
// re-identifiable record if it is shared. See .claude/CLAWHUB_STANDARDS.md
// (synthetic-test-data rule).
var realisticIdentifierPatterns = []struct {
	why string
	re  *regexp.Regexp
}{
	{"numeric Google user id (use the `users/me` alias instead)", regexp.MustCompile(`users/[0-9]`)},
	{"long opaque numeric resource id (use a short synthetic id instead)", regexp.MustCompile(`[0-9]{12,}`)},
}

// TestTestdataHasNoRealisticIdentifiers is the immutable guard for the fixture
// privacy finding. It walks testdata/ and fails if any committed fixture or
// golden contains a real-looking persistent identifier. Fix a failure by making
// the offending fixture synthetic — never by deleting or weakening this test.
func TestTestdataHasNoRealisticIdentifiers(t *testing.T) {
	root := filepath.Join(repoRoot(t), "testdata")
	err := filepath.WalkDir(root, func(path string, d os.DirEntry, err error) error {
		if err != nil {
			return err
		}
		if d.IsDir() {
			return nil
		}
		raw, rerr := os.ReadFile(path)
		if rerr != nil {
			return rerr
		}
		content := string(raw)
		rel, _ := filepath.Rel(root, path)
		for _, p := range realisticIdentifierPatterns {
			if loc := p.re.FindString(content); loc != "" {
				line := lineOf(content, loc)
				t.Errorf("testdata/%s contains a %s: %q (line %d) — committed test data must be synthetic",
					filepath.ToSlash(rel), p.why, loc, line)
			}
		}
		return nil
	})
	if err != nil {
		t.Fatalf("walk testdata: %v", err)
	}
}

// lineOf returns the 1-based line number of the first occurrence of sub in s.
func lineOf(s, sub string) int {
	i := strings.Index(s, sub)
	if i < 0 {
		return 0
	}
	return strings.Count(s[:i], "\n") + 1
}
