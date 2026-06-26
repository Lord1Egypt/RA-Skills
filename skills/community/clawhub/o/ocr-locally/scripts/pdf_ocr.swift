#!/usr/bin/env swift

import Foundation
import Quartz
import Vision
import CoreML
import CoreGraphics
import AppKit

class PDFOCRProcessor {
    let supportedLanguages = ["zh-hans", "zh-hant", "en", "ja", "ko", "fr", "de", "es", "it", "pt", "ru"]
    
    func processPDF(at path: String, pages: [Int]? = nil, languages: [String] = ["zh-hans", "zh-hant", "en"],
                    precise: Bool = true, jsonOutput: Bool = false) {
        let absolutePath = (path as NSString).expandingTildeInPath
        
        // 检查文件是否存在
        guard FileManager.default.fileExists(atPath: absolutePath) else {
            print("错误: PDF 文件不存在 - \(absolutePath)")
            exit(1)
        }
        
        // 加载 PDF
        let pdfURL = URL(fileURLWithPath: absolutePath)
        guard let pdfDocument = PDFDocument(url: pdfURL) else {
            print("错误: 无法加载 PDF 文件 - \(absolutePath)")
            exit(1)
        }
        
        let totalPages = pdfDocument.pageCount
        
        // 确定要处理的页面
        let pagesToProcess: [Int]
        if let specifiedPages = pages {
            pagesToProcess = specifiedPages.filter { $0 >= 1 && $0 <= totalPages }
            if pagesToProcess.isEmpty {
                print("错误: 指定的页面不在有效范围内 (1-\(totalPages))")
                exit(1)
            }
        } else {
            pagesToProcess = Array(1...totalPages)
        }
        
        if !jsonOutput {
            print("正在识别 PDF: \(absolutePath)")
            print("总页数: \(totalPages)")
            print("识别页数: \(pagesToProcess.count)")
            print("识别语言: \(languages.joined(separator: ", "))")
            print("识别模式: \(precise ? "精确" : "快速")")
            print()
        }
        
        // 处理每一页
        var allResults: [[String: Any]] = []
        
        for pageNum in pagesToProcess {
            guard let page = pdfDocument.page(at: pageNum - 1) else {
                continue
            }
            
            if !jsonOutput {
                print("正在识别第 \(pageNum) 页...")
            }
            
            // 将 PDF 页面渲染为图像
            guard let cgImage = renderPDFPageToImage(page: page) else {
                print("警告: 无法渲染第 \(pageNum) 页")
                continue
            }
            
            // 对当前页面进行 OCR
            let pageResult = performOCR(on: cgImage, pageNum: pageNum, languages: languages, precise: precise)
            allResults.append(pageResult)
        }
        
        // 输出结果
        if jsonOutput {
            outputJSON(results: allResults, pdfPath: absolutePath, totalPages: totalPages)
        } else {
            outputText(results: allResults)
        }
    }
    
    func renderPDFPageToImage(page: PDFPage) -> CGImage? {
        let pageRect = page.bounds(for: .mediaBox)
        
        // 创建图像上下文
        let width = Int(pageRect.width)
        let height = Int(pageRect.height)
        
        guard let context = CGContext(data: nil,
                                     width: width,
                                     height: height,
                                     bitsPerComponent: 8,
                                     bytesPerRow: 0,
                                     space: CGColorSpaceCreateDeviceRGB(),
                                     bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue) else {
            return nil
        }
        
        // 设置白色背景
        context.setFillColor(red: 1.0, green: 1.0, blue: 1.0, alpha: 1.0)
        context.fill(CGRect(x: 0, y: 0, width: width, height: height))
        
        // 渲染 PDF 页面到上下文（PDFKit 会处理坐标转换）
        page.draw(with: .mediaBox, to: context)
        
        // 获取 CGImage
        return context.makeImage()
    }
    
    func performOCR(on cgImage: CGImage, pageNum: Int, languages: [String], precise: Bool) -> [String: Any] {
        var pageResult: [String: Any] = [:]
        pageResult["pageNumber"] = pageNum
        pageResult["blocks"] = []
        
        let semaphore = DispatchSemaphore(value: 0)
        
        let request = VNRecognizeTextRequest { (request, error) in
            if let error = error {
                print("识别错误 (第 \(pageNum) 页): \(error.localizedDescription)")
                semaphore.signal()
                return
            }
            
            guard let observations = request.results as? [VNRecognizedTextObservation] else {
                semaphore.signal()
                return
            }
            
            var blocks: [[String: Any]] = []
            var fullText = ""
            
            for (index, observation) in observations.enumerated() {
                let candidates = observation.topCandidates(1)
                
                if let candidate = candidates.first {
                    let boundingBox = observation.boundingBox
                    
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
                    fullText += candidate.string + "\n"
                }
            }
            
            pageResult["blocks"] = blocks
            pageResult["text"] = fullText.trimmingCharacters(in: .whitespacesAndNewlines)
            pageResult["blockCount"] = blocks.count
            
            let confidences = blocks.compactMap { $0["confidence"] as? Float }
            if !confidences.isEmpty {
                pageResult["averageConfidence"] = confidences.reduce(0, +) / Float(confidences.count)
            }
            
            semaphore.signal()
        }
        
        request.recognitionLanguages = languages
        request.recognitionLevel = precise ? .accurate : .fast
        request.usesLanguageCorrection = true
        
        let handler = VNImageRequestHandler(cgImage: cgImage, options: [:])
        
        do {
            try handler.perform([request])
        } catch {
            print("执行识别失败 (第 \(pageNum) 页): \(error.localizedDescription)")
        }
        
        semaphore.wait()
        
        return pageResult
    }
    
    func outputJSON(results: [[String: Any]], pdfPath: String, totalPages: Int) {
        var output: [String: Any] = [:]
        output["pdfPath"] = pdfPath
        output["totalPages"] = totalPages
        output["processedPages"] = results.count
        output["pages"] = results
        
        do {
            let jsonData = try JSONSerialization.data(withJSONObject: output, options: [.prettyPrinted, .sortedKeys])
            if let jsonString = String(data: jsonData, encoding: .utf8) {
                print(jsonString)
            }
        } catch {
            print("错误: 无法生成 JSON - \(error.localizedDescription)")
            exit(1)
        }
    }
    
    func outputText(results: [[String: Any]]) {
        for result in results {
            let pageNum = result["pageNumber"] as? Int ?? 0
            let text = result["text"] as? String ?? ""
            
            print("\n=== 第 \(pageNum) 页 ===\n")
            print(text)
        }
    }
}

// 打印使用说明
func printUsage() {
    print("""
    用法: pdf_ocr.swift <PDF路径> [选项]
    
    输出模式 (互斥):
      -t, --text           文本模式 (默认, 只输出识别文本)
      -j, --json           JSON 模式 (输出包含文字、位置和置信度的完整原始信息)
    
    页面选择:
      -p, --pages <页码>   指定要识别的页面 (默认: 全部页面)
                           支持格式: 1,3,5 或 1-5
    
    选项:
      -l, --language <语言>       指定识别语言 (默认: zh-hans,zh-hant,en)
                                  支持: zh-hans, zh-hant, en, ja, ko, fr, de, es, it, pt, ru
      -f, --fast                 使用快速模式 (默认: 精确模式)
      -h, --help                 显示帮助信息
    
    示例:
      pdf_ocr.swift document.pdf              # 识别所有页面
      pdf_ocr.swift document.pdf -p 1        # 只识别第 1 页
      pdf_ocr.swift document.pdf -p 1,3,5    # 识别第 1, 3, 5 页
      pdf_ocr.swift document.pdf -j           # JSON 模式输出
      pdf_ocr.swift document.pdf -p 1 -j     # 识别第 1 页并 JSON 模式输出
    
    输出说明:
      - 文本模式 (-t): 按页输出识别后的文本
      - JSON 模式 (-j): 输出包含以下信息的 JSON:
        * pdfPath: PDF 文件路径
        * totalPages: 总页数
        * processedPages: 已处理页数
        * pages: 每页的详细信息 (页码、文字、置信度、位置)
      - JSON 模式输出到标准输出，不包含其他信息
      - 两种模式互斥，不能同时启用
    
    依赖: 需要 macOS 10.4+ (PDFKit 框架)
    """)
}

// 解析页面参数
func parsePages(_ pageString: String, totalPages: Int) -> [Int]? {
    var pages: [Int] = []
    
    let components = pageString.split(separator: ",")
    for component in components {
        let trimmed = component.trimmingCharacters(in: .whitespaces)
        
        if trimmed.contains("-") {
            // 页码范围
            let rangeParts = trimmed.split(separator: "-")
            if rangeParts.count == 2,
               let start = Int(rangeParts[0].trimmingCharacters(in: .whitespaces)),
               let end = Int(rangeParts[1].trimmingCharacters(in: .whitespaces)) {
                for page in start...min(end, totalPages) {
                    if page >= 1 {
                        pages.append(page)
                    }
                }
            }
        } else {
            // 单个页码
            if let page = Int(trimmed) {
                if page >= 1 && page <= totalPages {
                    pages.append(page)
                }
            }
        }
    }
    
    return pages.isEmpty ? nil : pages.sorted()
}

// 解析命令行参数
var pdfPath: String?
var pages: [Int]?
var languages = ["zh-hans", "zh-hant", "en"]
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
        jsonOutput = false
        
    case "-p", "--pages":
        i += 1
        if i < CommandLine.arguments.count {
            let pageString = CommandLine.arguments[i]
            // 需要先加载 PDF 才能解析页面参数
            let tempPath = pdfPath ?? ""
            let tempAbsolutePath = (tempPath as NSString).expandingTildeInPath
            if let tempURL = URL(string: "file://\(tempAbsolutePath)"),
               let tempDoc = PDFDocument(url: tempURL) {
                pages = parsePages(pageString, totalPages: tempDoc.pageCount)
            }
        }
        
    case "-l", "--language":
        i += 1
        if i < CommandLine.arguments.count {
            languages = CommandLine.arguments[i].split(separator: ",").map { String($0).trimmingCharacters(in: .whitespaces).lowercased() }
        }
        
    case "-f", "--fast":
        precise = false
        
    default:
        if pdfPath == nil {
            pdfPath = arg
        }
    }
    
    i += 1
}

// 检查是否提供了 PDF 路径
guard let path = pdfPath else {
    print("错误: 未指定 PDF 路径")
    print()
    printUsage()
    exit(1)
}

// 如果指定了页面参数，需要重新解析（因为需要知道总页数）
if let pageArgIndex = CommandLine.arguments.firstIndex(where: { $0 == "-p" || $0 == "--pages" }) {
    if pageArgIndex + 1 < CommandLine.arguments.count {
        let pageString = CommandLine.arguments[pageArgIndex + 1]
        let absolutePath = (path as NSString).expandingTildeInPath
        if let pdfURL = URL(string: "file://\(absolutePath)"),
           let pdfDocument = PDFDocument(url: pdfURL) {
            pages = parsePages(pageString, totalPages: pdfDocument.pageCount)
        }
    }
}

// 执行 OCR
let processor = PDFOCRProcessor()
processor.processPDF(at: path, pages: pages, languages: languages, precise: precise, jsonOutput: jsonOutput)
