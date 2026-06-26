#!/usr/bin/env swift

import Vision
import CoreML
import CoreGraphics
import Foundation
import AppKit

// 检查命令行参数
guard CommandLine.arguments.count > 1 else {
    print("用法: \(CommandLine.arguments[0]) <图片路径>")
    print("支持格式: PNG, JPEG, TIFF, BMP, PDF")
    exit(1)
}

let imagePath = CommandLine.arguments[1]
let fileManager = FileManager.default
let absolutePath = (imagePath as NSString).expandingTildeInPath

// 检查文件是否存在
guard fileManager.fileExists(atPath: absolutePath) else {
    print("错误: 文件不存在 - \(absolutePath)")
    exit(1)
}

// 加载图片
guard let image = NSImage(contentsOfFile: absolutePath) else {
    print("错误: 无法加载图片 - \(absolutePath)")
    exit(1)
}

// 转换 NSImage 为 CGImage
guard let tiffData = image.tiffRepresentation,
      let bitmapImage = NSBitmapImageRep(data: tiffData),
      let cgImage = bitmapImage.cgImage else {
    print("错误: 无法转换图片格式")
    exit(1)
}

// 创建 OCR 请求
let request = VNRecognizeTextRequest { (request, error) in
    if let error = error {
        print("识别错误: \(error.localizedDescription)")
        return
    }
    
    guard let observations = request.results as? [VNRecognizedTextObservation] else {
        print("错误: 无法获取识别结果")
        return
    }
    
    if observations.isEmpty {
        print("未检测到文字")
        return
    }
    
    print("\n=== 识别结果 ===\n")
    
    for (index, observation) in observations.enumerated() {
        // 获取最优识别结果
        let candidates = observation.topCandidates(1)
        
        if let candidate = candidates.first {
            let boundingBox = observation.boundingBox
            print("[\(index + 1)] \(candidate.string)")
            print("    置信度: \(String(format: "%.2f", candidate.confidence))")
            print("    位置: x=\(String(format: "%.2f", boundingBox.origin.x)), y=\(String(format: "%.2f", boundingBox.origin.y)), w=\(String(format: "%.2f", boundingBox.width)), h=\(String(format: "%.2f", boundingBox.height))")
            print()
        }
    }
    
    // 输出完整文本
    print("=== 完整文本 ===\n")
    let fullText = observations.compactMap { $0.topCandidates(1).first?.string }.joined(separator: "\n")
    print(fullText)
}

// 配置 OCR 参数
request.recognitionLanguages = ["zh-Hans", "zh-Hant", "en"]  // 支持中文和英文
request.recognitionLevel = .accurate  // 使用精确模式
request.usesLanguageCorrection = true  // 启用语言纠正

// 创建请求处理器
let handler = VNImageRequestHandler(cgImage: cgImage, options: [:])

do {
    print("正在识别图片: \(absolutePath)")
    try handler.perform([request])
} catch {
    print("执行识别失败: \(error.localizedDescription)")
    exit(1)
}
