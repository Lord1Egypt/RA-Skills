//go:build windows

package cmd

import (
	"fmt"
	"os"
	"path/filepath"
	"syscall"
	"unsafe"
)

func getStatfs(path string) (total, free int64, err error) {
	absPath, err := filepath.Abs(path)
	if err != nil {
		return 0, 0, err
	}
	if _, err := os.Stat(absPath); err != nil {
		return 0, 0, err
	}
	kernel32 := syscall.NewLazyDLL("kernel32.dll")
	getDiskFreeSpaceEx := kernel32.NewProc("GetDiskFreeSpaceExW")
	pathPtr, _ := syscall.UTF16PtrFromString(absPath)
	var freeBytesAvailable, totalBytes, totalFreeBytes int64
	r1, _, e1 := getDiskFreeSpaceEx.Call(
		uintptr(unsafe.Pointer(pathPtr)),
		uintptr(unsafe.Pointer(&freeBytesAvailable)),
		uintptr(unsafe.Pointer(&totalBytes)),
		uintptr(unsafe.Pointer(&totalFreeBytes)),
	)
	if r1 == 0 {
		return 0, 0, fmt.Errorf("GetDiskFreeSpaceExW: %v", e1)
	}
	return totalBytes, freeBytesAvailable, nil
}
