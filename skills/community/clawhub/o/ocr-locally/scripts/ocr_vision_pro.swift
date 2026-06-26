#!/usr/bin/env swift

import Vision
import CoreML
import CoreGraphics
import Foundation
import AppKit

class OCRProcessor {
    let supportedLanguages = ["zh-Hans", "zh-Hant", "en", "ja", "ko", "fr", "de", "es", "it", "pt", "ru"]
    
    func processImage(at path: String, languages: [String] = ["zh-Hans", "zh-Hant", "en"], 
                     textOutputPath: String? = nil, confidenceOutputPath: String? = nil,
                     precise: Bool = true, jsonOutput: Bool = false) {
        let absolutePath = (path as NSString).expandingTildeInPath
        
        // 检查文件是否存在
        guard FileManager.default.fileExists(atPath: absolutePath) else {
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
        let request = VNRecognizeTextRequest { [weak self] (request, error) in
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
            
            if jsonOutput {
                // JSON 模式：输出完整的原始信息
                self?.outputJSON(observations: observations, imagePath: absolutePath)
            } else {
                // 纯文本模式：只输出识别后的文本
                self?.outputTextOnly(observations: observations, 
                                   textOutputPath: textOutputPath, 
                                   confidenceOutputPath: confidenceOutputPath)
            }
        }
        
        // 配置 OCR 参数
        request.recognitionLanguages = languages
        request.recognitionLevel = precise ? .accurate : .fast
        request.usesLanguageCorrection = true
        
        // 创建请求处理器
        let handler = VNImageRequestHandler(cgImage: cgImage, options: [:])
        
        do {
            if !jsonOutput {
                print("正在识别图片: \(absolutePath)")
                print("识别语言: \(languages.joined(separator: ", "))")
                print("识别模式: \(precise ? "精确" : "快速")")
                print()
            }
            try handler.perform([request])
        } catch {
            print("执行识别失败: \(error.localizedDescription)")
            exit(1)
        }
    }
    
    // MARK: - JSON 输出模式
    
    func outputJSON(observations: [VNRecognizedTextObservation], imagePath: String) {
        var blocks: [[String: Any]] = []
        
        for (index, observation) in observations.enumerated() {
            let candidates = observation.topCandidates(1)
            
            if let candidate = candidates.first {
                let boundingBox = observation.boundingBox
                
                // 构建每个文本块的信息
                var block: [String: Any] = [:]
                block["index"] = index + 1
                block["text"] = candidate.string
                block["confidence"] = candidate.confidence
                block["boundingBox"] = [
                    "x": boundingBox.origin.x,
                    "y": boundingBox.origin.y,
                    "width": boundingBox.width,
                    "height": boundingBox.height
                ]
                
                blocks.append(block)
            }
        }
        
        // 构建完整的 JSON 结构
        var result: [String: Any] = [:]
        result["imagePath"] = imagePath
        result["totalBlocks"] = observations.count
        
        let confidences = observations.compactMap { $0.topCandidates(1).first?.confidence }
        let avgConfidence = confidences.reduce(0, +) / Float(confidences.count)
        result["averageConfidence"] = avgConfidence
        result["blocks"] = blocks
        
        // 转换为 JSON 字符串
        do {
            let jsonData = try JSONSerialization.data(withJSONObject: result, options: [.prettyPrinted, .sortedKeys])
            if let jsonString = String(data: jsonData, encoding: .utf8) {
                print(jsonString)
            }
        } catch {
            print("错误: 无法生成 JSON - \(error.localizedDescription)")
            exit(1)
        }
    }
    
    // MARK: - 纯文本输出模式
    
    func outputTextOnly(observations: [VNRecognizedTextObservation], 
                       textOutputPath: String? = nil, 
                       confidenceOutputPath: String? = nil) {
        // 构建置信度信息
        var confidenceText = "=== 置信度详情 ===\n\n"
        let confidences = observations.compactMap { $0.topCandidates(1).first?.confidence }
        let avgConfidence = confidences.reduce(0, +) / Float(confidences.count)
        confidenceText += "总识别块数: \(observations.count)\n"
        confidenceText += "平均置信度: \(String(format: "%.2f", avgConfidence))\n\n"
        confidenceText += "--- 逐块详情 ---\n\n"
        
        var lowConfidenceBlocks: [(Int, String, Float)] = []
        
        for (index, observation) in observations.enumerated() {
            let candidates = observation.topCandidates(1)
            
            if let candidate = candidates.first {
                let boundingBox = observation.boundingBox
                confidenceText += "[\(index + 1)] \(candidate.string)\n"
                confidenceText += "    置信度: \(String(format: "%.2f", candidate.confidence))\n"
                confidenceText += "    位置: x=\(String(format: "%.2f", boundingBox.origin.x)), y=\(String(format: "%.2f", boundingBox.origin.y)), w=\(String(format: "%.2f", boundingBox.width)), h=\(String(format: "%.2f", boundingBox.height))\n\n"
                
                // 记录低置信度块
                if candidate.confidence < 0.8 {
                    lowConfidenceBlocks.append((index + 1, candidate.string, candidate.confidence))
                }
            }
        }
        
        // 输出低置信度警告
        if !lowConfidenceBlocks.isEmpty {
            confidenceText += "--- 低置信度警告 (< 0.8) ---\n"
            for (index, text, conf) in lowConfidenceBlocks {
                confidenceText += "[\(index)] \"\(text)\" - 置信度: \(String(format: "%.2f", conf))\n"
            }
        }
        
        // 构建完整文本
        let fullText = observations.compactMap { $0.topCandidates(1).first?.string }.joined(separator: "\n")
        
        // 处理输出路径
        if let textPath = textOutputPath, let confPath = confidenceOutputPath {
            // 分别输出到指定文件
            self.writeToFile(text: fullText, path: textPath)
            self.writeToFile(text: confidenceText, path: confPath)
        } else if let textPath = textOutputPath {
            // 只输出文本文件，自动生成置信度文件名
            let basePath = (textPath as NSString).deletingPathExtension
            let confidencePath = basePath + "_confidence.txt"
            
            self.writeToFile(text: fullText, path: textPath)
            self.writeToFile(text: confidenceText, path: confidencePath)
        } else if let confPath = confidenceOutputPath {
            // 只输出置信度信息到指定文件
            self.writeToFile(text: confidenceText, path: confPath)
        } else {
            // 输出到控制台 - 只输出纯文本
            print(fullText)
        }
    }
    
    // MARK: - 辅助方法
    
    func writeToFile(text: String, path: String) {
        let absolutePath = (path as NSString).expandingTildeInPath
        do {
            try text.write(toFile: absolutePath, atomically: true, encoding: .utf8)
            print("已保存: \(absolutePath)")
        } catch {
            print("错误: 无法写入文件 - \(error.localizedDescription)")
            exit(1)
        }
    }
}

// 打印使用说明
func printUsage() {
    print("""
    用法: ocr_vision_pro.swift <图片路径> [选项]
    
    输出模式 (互斥):
      -t, --text           纯文本模式 (默认, 只输出识别文本)
      -j, --json           JSON 模式 (输出包含文字、位置和置信度的完整原始信息)
    
    选项:
      -l, --language <语言>       指定识别语言 (默认: zh-Hans,zh-Hant,en)
                                  支持: zh-Hans, zh-Hant, en, ja, ko, fr, de, es, it, pt, ru
      -o, --output <文件路径>     输出完整文本到文件 (自动生成 *_confidence.txt 保存置信度信息)
      -t, --text <文件路径>       只输出完整文本到指定文件 (纯文本模式)
      -c, --confidence <文件路径> 只输出置信度信息到指定文件 (纯文本模式)
      -f, --fast                 使用快速模式 (默认: 精确模式)
      -h, --help                 显示帮助信息
    
    示例:
      ocr_vision_pro.swift image.png              # 纯文本模式 (默认)
      ocr_vision_pro.swift image.png -j           # JSON 模式
      ocr_vision_pro.swift image.jpg -o result.txt
      ocr_vision_pro.swift image.png -t text_only.txt -c confidence.txt
      ocr_vision_pro.swift image.png -f -j
    
    输出说明:
      - 纯文本模式 (-t): 只输出识别后的文本，或保存到指定文件
      - JSON 模式 (-j): 输出包含以下信息的 JSON:
        * imagePath: 图片路径
        * totalBlocks: 总识别块数
        * averageConfidence: 平均置信度
        * blocks: 每个文本块的详细信息 (文字、置信度、位置)
      - JSON 模式输出到标准输出，不包含其他信息
      - 两种模式互斥，不能同时启用
    
    支持格式: PNG, JPEG, TIFF, BMP, PDF
    """)
}

// 解析命令行参数
var imagePath: String?
var languages = ["zh-Hans", "zh-Hant", "en"]
var textOutputPath: String?
var confidenceOutputPath: String?
var precise = true
var jsonOutput = false

var i = 1
while i < CommandLine.arguments.count {
    let arg = CommandLine.arguments[i]
    
    switch arg {
    case "-h", "--help":
        printUsage()
        exit(0)
        
    case "-j", "--json":
        jsonOutput = true
        
    case "-t", "--text":
        // 如果是纯文本模式且没有指定文件路径，只是设置模式
        if i + 1 < CommandLine.arguments.count && !CommandLine.arguments[i + 1].hasPrefix("-") {
            i += 1
            textOutputPath = CommandLine.arguments[i]
        }
        // 如果 -t 后面没有参数，只是设置纯文本模式（默认）
        jsonOutput = false
        
    case "-l", "--language":
        i += 1
        if i < CommandLine.arguments.count {
            languages = CommandLine.arguments[i].split(separator: ",").map { String($0) }
        }
        
    case "-o", "--output":
        i += 1
        if i < CommandLine.arguments.count {
            textOutputPath = CommandLine.arguments[i]
        }
        
    case "-c", "--confidence":
        i += 1
        if i < CommandLine.arguments.count {
            confidenceOutputPath = CommandLine.arguments[i]
        }
        
    case "-f", "--fast":
        precise = false
        
    default:
        if imagePath == nil {
            imagePath = arg
        }
    }
    
    i += 1
}

// 检查是否提供了图片路径
guard let path = imagePath else {
    print("错误: 未指定图片路径")
    print()
    printUsage()
    exit(1)
}

// 执行 OCR
let processor = OCRProcessor()
processor.processImage(at: path, languages: languages, 
                     textOutputPath: textOutputPath, 
                     confidenceOutputPath: confidenceOutputPath,
                     precise: precise,
                     jsonOutput: jsonOutput)
