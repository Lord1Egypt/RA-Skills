import Cocoa
import ApplicationServices

func getAllWindowTitles() -> [[String: String]] {
    var results: [[String: String]] = []
    let apps = NSRunningApplication.runningApplications(withBundleIdentifier: "")
    
    for app in NSWorkspace.shared.runningApplications {
        guard app.activationPolicy == .regular else { continue }
        let appElem = AXUIElementCreateApplication(app.processIdentifier)
        
        var windowList: CFTypeRef?
        let result = AXUIElementCopyAttributeValue(appElem, kAXWindowsAttribute as CFString, &windowList)
        guard result == .success, let windows = windowList as? [AXUIElement] else { continue }
        
        for win in windows {
            var titleRef: CFTypeRef?
            AXUIElementCopyAttributeValue(win, kAXTitleAttribute as CFString, &titleRef)
            let title = (titleRef as? String) ?? ""
            if !title.isEmpty {
                results.append([
                    "app": app.localizedName ?? "Unknown",
                    "title": title
                ])
            }
        }
    }
    return results
}

// Request permission if needed
let options: NSDictionary = [kAXTrustedCheckOptionPrompt.takeRetainedValue() as NSString: true]
let trusted = AXIsProcessTrustedWithOptions(options)

if trusted {
    let windows = getAllWindowTitles()
    if let data = try? JSONSerialization.data(withJSONObject: windows, options: []),
       let str = String(data: data, encoding: .utf8) {
        print(str)
    }
} else {
    print("[]")
}
