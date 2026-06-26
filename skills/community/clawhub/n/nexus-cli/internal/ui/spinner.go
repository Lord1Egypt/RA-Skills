package ui

import (
	"fmt"
	"os"
	"strings"
	"time"
)

// SpinWhile shows an animated spinner while fn runs, then prints the result.
func SpinWhile(msg string, fn func() error) error {
	// TTY guard: skip animation if stderr is not a terminal
	isTTY := true
	if stat, err := os.Stderr.Stat(); err == nil {
		if stat.Mode()&os.ModeCharDevice == 0 {
			isTTY = false
		}
	}

	if !isTTY {
		fmt.Fprintf(os.Stderr, "  … %s\n", msg)
		err := fn()
		if err != nil {
			fmt.Fprintf(os.Stderr, "  %s %s: %s\n", Err("✗"), msg, err)
		} else {
			fmt.Fprintf(os.Stderr, "  %s %s\n", Ok("✓"), msg)
		}
		return err
	}

	frames := []string{"⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"}
	done := make(chan struct{})
	ticker := time.NewTicker(80 * time.Millisecond)

	go func() {
		i := 0
		for {
			select {
			case <-done:
				ticker.Stop()
				return
			case <-ticker.C:
				fmt.Fprintf(os.Stderr, "\r  %s %s", frames[i%len(frames)], msg)
				i++
			}
		}
	}()

	err := fn()
	close(done)

	// Clear the line
	clearLine := "\r" + strings.Repeat(" ", len(msg)+10) + "\r"
	fmt.Fprint(os.Stderr, clearLine)

	if err != nil {
		fmt.Fprintf(os.Stderr, "  %s %s: %s\n", Err("✗"), msg, err)
	} else {
		fmt.Fprintf(os.Stderr, "  %s %s\n", Ok("✓"), msg)
	}

	return err
}
