import AppKit

let root = URL(fileURLWithPath: FileManager.default.currentDirectoryPath)
let source = root.appendingPathComponent("assets/editorial-visual.png")
let output = root.appendingPathComponent("assets/promo-1600x900.png")
guard let image = NSImage(contentsOf: source) else { fatalError("Cannot load illustration") }
let width = 1600, height = 900
guard let bitmap = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: width, pixelsHigh: height, bitsPerSample: 8, samplesPerPixel: 4, hasAlpha: true, isPlanar: false, colorSpaceName: .deviceRGB, bytesPerRow: 0, bitsPerPixel: 0) else { fatalError("Cannot create canvas") }
let context = NSGraphicsContext(bitmapImageRep: bitmap)!
NSGraphicsContext.saveGraphicsState()
NSGraphicsContext.current = context
image.draw(in: NSRect(x: 0, y: 0, width: width, height: height))
NSColor(calibratedRed: 0.969, green: 0.953, blue: 0.925, alpha: 0.90).setFill()
NSBezierPath(rect: NSRect(x: 0, y: 0, width: 880, height: 900)).fill()
NSColor(calibratedRed: 0.941, green: 0.475, blue: 0.408, alpha: 1).setFill()
NSBezierPath(roundedRect: NSRect(x: 105, y: 669, width: 92, height: 8), xRadius: 4, yRadius: 4).fill()
func label(_ value: String, at point: NSPoint, size: CGFloat, color: NSColor, weight: NSFont.Weight) {
    let font = NSFont.systemFont(ofSize: size, weight: weight)
    value.draw(at: point, withAttributes: [.font: font, .foregroundColor: color])
}
let navy = NSColor(calibratedRed: 0.09, green: 0.227, blue: 0.369, alpha: 1)
let grey = NSColor(calibratedRed: 0.369, green: 0.408, blue: 0.447, alpha: 1)
label("读者反馈", at: NSPoint(x: 105, y: 560), size: 76, color: navy, weight: .bold)
label("改稿待办", at: NSPoint(x: 105, y: 465), size: 76, color: navy, weight: .bold)
label("去重意见，马上开改", at: NSPoint(x: 105, y: 395), size: 30, color: grey, weight: .regular)
NSColor(calibratedRed: 0.843, green: 0.816, blue: 0.773, alpha: 1).setStroke()
let line = NSBezierPath(); line.move(to: NSPoint(x: 105, y: 345)); line.line(to: NSPoint(x: 620, y: 345)); line.lineWidth = 2; line.stroke()
label("问题组 · 影响章节 · 优先清单", at: NSPoint(x: 105, y: 285), size: 24, color: grey, weight: .regular)
NSGraphicsContext.restoreGraphicsState()
guard let png = bitmap.representation(using: .png, properties: [:]) else { fatalError("Cannot encode PNG") }
try png.write(to: output)

guard let icon = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: 512, pixelsHigh: 512, bitsPerSample: 8, samplesPerPixel: 4, hasAlpha: true, isPlanar: false, colorSpaceName: .deviceRGB, bytesPerRow: 0, bitsPerPixel: 0) else { fatalError("Cannot create icon") }
let iconContext = NSGraphicsContext(bitmapImageRep: icon)!
NSGraphicsContext.saveGraphicsState()
NSGraphicsContext.current = iconContext
image.draw(in: NSRect(x: 0, y: 0, width: 512, height: 512), from: NSRect(x: 731, y: 0, width: 941, height: 941), operation: .copy, fraction: 1)
NSGraphicsContext.restoreGraphicsState()
guard let iconPNG = icon.representation(using: .png, properties: [:]) else { fatalError("Cannot encode icon") }
try iconPNG.write(to: root.appendingPathComponent("icon-512.png"))
