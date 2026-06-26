# literature_review_polisher.R
# 文献综述润色与查缺补漏助手 - 完整版（含学历选择 + Kimi API + 自动保存）

library(stringr)
library(magrittr)
library(httr)
library(jsonlite)

# ========== 请在这里填写你的API信息 ==========
KIMI_API_KEY <- "sk-kwe4WnYviimoCDIXOXgG82Xh91c9hWSNNobXj3OMUvfabOSF"
KIMI_BASE_URL <- "https://api.moonshot.cn/v1"
# ===========================================

# 调用Kimi API进行润色
polish_with_kimi <- function(text, instruction, academic_level) {
  url <- paste0(KIMI_BASE_URL, "/chat/completions")
  
  # 根据学历调整提示词
  level_prompt <- switch(academic_level,
    "本科" = "语言简洁明了，适合本科毕业论文水平。",
    "硕士" = "语言规范学术化，体现一定的理论深度。",
    "博士/科研" = "语言精炼严谨，体现创新性和批判性思维。"
  )
  
  system_prompt <- sprintf("你是一位专业的学术论文编辑，擅长润色文献综述。请保持原意和引用信息不变。%s", level_prompt)
  
  user_prompt <- sprintf("
请根据以下要求润色这段文献综述：

要求：%s

原文：
%s

请直接输出润色后的段落，不要加额外说明。
", instruction, text)
  
  body <- list(
    model = "moonshot-v1-8k",
    messages = list(
      list(role = "system", content = system_prompt),
      list(role = "user", content = user_prompt)
    ),
    temperature = 0.7
  )
  
  response <- POST(
    url,
    add_headers(
      "Authorization" = paste("Bearer", KIMI_API_KEY),
      "Content-Type" = "application/json"
    ),
    body = toJSON(body, auto_unbox = TRUE),
    encode = "json"
  )
  
  if (status_code(response) == 200) {
    result <- fromJSON(content(response, "text", encoding = "UTF-8"))
    return(result$choices$message$content)
  } else {
    return(paste("❌ API调用失败：", content(response, "text")))
  }
}

# 分析文献综述
analyze_review <- function(text, academic_level) {
  length <- nchar(text)
  
  structure_check <- list(
    研究背景 = grepl("背景|问题提出|研究意义", text),
    概念界定 = grepl("定义|概念|内涵|界定", text),
    发展脉络 = grepl("发展|历程|演变|历史|早期|近年来", text),
    观点分类 = grepl("一类|另一种|主流观点|可分为|主要分为", text),
    争议焦点 = grepl("争议|分歧|争论|不同观点|矛盾", text),
    研究空白 = grepl("不足|局限|空缺|有待|尚未|缺乏", text)
  )
  
  citations <- str_extract_all(text, "\\([^)]*\\d{4}[^)]*\\)|（[^）]*\\d{4}[^）]*）|et al\\.|等人")
  citation_count <- ifelse(length(citations[[1]]) == 0, 0, length(citations[[1]]))
  citation_density <- citation_count / (length / 100)
  
  listing_count <- str_count(text, "指出|认为|提出|表明|发现")
  has_critical <- grepl("但是|然而|不过|相比之下", text)
  
  suggestions <- c()
  
  if (citation_density < 0.5) {
    suggestions <- c(suggestions, "⚠️ 引用密度较低，建议增加文献支撑")
  } else if (citation_density > 3) {
    suggestions <- c(suggestions, "⚠️ 引用过于密集，可能存在堆砌问题")
  }
  
  missing <- names(structure_check)[!unlist(structure_check)]
  if (length(missing) > 0) {
    suggestions <- c(suggestions, paste0("📋 缺少结构要素：", paste(missing, collapse = ", ")))
  }
  
  if (listing_count > 10 && !has_critical) {
    suggestions <- c(suggestions, "🔄 检测到观点罗列模式，需要增加对比和批判性分析")
  }
  
  critical_keywords <- c("然而", "但是", "相比之下", "值得注意的是", "局限性", "不足", "质疑", "挑战")
  critical_score <- min(10, sum(sapply(critical_keywords, function(kw) grepl(kw, text))) * 2)
  
  # 根据学历调整评分标准
  if (academic_level == "本科") {
    critical_score <- min(10, critical_score + 1)  # 本科标准稍宽松
  } else if (academic_level == "博士/科研") {
    critical_score <- max(0, critical_score - 1)   # 博士标准更严格
  }
  
  # 生成润色重点提示
  polish_instruction <- ""
  if (critical_score < 6) {
    polish_instruction <- paste(polish_instruction, "增加批判性对比分析，避免简单罗列观点。")
  }
  if (length(missing) > 0 && "争议焦点" %in% missing) {
    polish_instruction <- paste(polish_instruction, "补充该领域的争议焦点讨论。")
  }
  if (length(missing) > 0 && "研究空白" %in% missing) {
    polish_instruction <- paste(polish_instruction, "明确指出现有研究的不足和本研究的定位。")
  }
  if (academic_level == "博士/科研" && critical_score < 7) {
    polish_instruction <- paste(polish_instruction, "需要更强的创新性和批判性深度。")
  }
  
  return(list(
    length = length,
    has_structure = structure_check,
    citation_density = citation_density,
    critical_score = critical_score,
    suggestions = suggestions,
    missing = missing,
    polish_instruction = polish_instruction
  ))
}

# 生成润色报告（含具体润色结果 + 自动保存）
generate_full_report <- function(original_text, academic_level) {
  cat("\n🔍 正在分析您的文献综述...\n")
  analysis <- analyze_review(original_text, academic_level)
  
  cat("\n📊 分析结果：\n")
  cat(rep("-", 50), "\n", sep = "")
  cat(sprintf("学术水平: %s\n", academic_level))
  cat(sprintf("字数: %d字\n", analysis$length))
  cat(sprintf("引用密度: %.1f次/100字\n", analysis$citation_density))
  cat(sprintf("批判性评分: %d/10\n", analysis$critical_score))
  
  cat("\n📋 结构检查：\n")
  if (length(analysis$missing) > 0) {
    cat(sprintf("   ❌ 缺失: %s\n", paste(analysis$missing, collapse = ", ")))
  } else {
    cat("   ✅ 结构完整\n")
  }
  
  if (length(analysis$suggestions) > 0) {
    cat("\n💡 改进建议：\n")
    for (s in analysis$suggestions) {
      cat(sprintf("   %s\n", s))
    }
  }
  
  cat("\n", rep("=", 60), "\n", sep = "")
  cat("🤖 开始AI润色...\n")
  cat(rep("=", 60), "\n", sep = "")
  
  # 调用Kimi API进行润色
  if (nchar(analysis$polish_instruction) < 5) {
    analysis$polish_instruction <- "提升学术性和逻辑连贯性，保持原意不变。"
  }
  
  polished <- polish_with_kimi(original_text, analysis$polish_instruction, academic_level)
  
  # 保存到文件
  timestamp <- format(Sys.time(), "%Y%m%d_%H%M%S")
  output_filename <- paste0("polished_", academic_level, "_", timestamp, ".txt")
  writeLines(polished, output_filename, useBytes = TRUE)
  
  cat("\n✨ 润色后的版本：\n")
  cat(rep("-", 50), "\n", sep = "")
  cat(polished)
  cat("\n", rep("-", 50), "\n", sep = "")
  
  # 提示文件保存位置
  cat("\n💾 润色结果已自动保存到文件：", output_filename, "\n")
  cat("   文件位置：", getwd(), "/", output_filename, "\n", sep = "")
  
  return(list(
    original = original_text,
    polished = polished,
    analysis = analysis
  ))
}

# 测试API连接
test_api <- function() {
  cat("🔌 测试Kimi API连接...\n")
  test_text <- "这是一段测试文本。"
  result <- polish_with_kimi(test_text, "直接返回原文即可，测试连接。", "硕士")
  
  if (grepl("❌", result)) {
    cat(result, "\n")
    cat("\n⚠️ 请检查：\n")
    cat("1. API Key是否正确\n")
    cat("2. 是否有网络问题\n")
  } else {
    cat("✅ API连接成功！\n")
  }
}

# 选择学历
select_academic_level <- function() {
  cat("\n请选择您的学术水平：\n")
  cat("1. 本科\n")
  cat("2. 硕士\n")
  cat("3. 博士/科研\n")
  
  choice <- readline(prompt = "\n请输入数字 (1/2/3): ")
  
  level_map <- list(
    "1" = "本科",
    "2" = "硕士",
    "3" = "博士/科研"
  )
  
  level <- level_map[[choice]]
  if (is.null(level)) {
    cat("输入无效，默认使用【硕士】级别\n")
    level <- "硕士"
  }
  
  cat(sprintf("\n✅ 已设置为【%s】级别\n", level))
  return(level)
}

# 交互式使用
run_interactive <- function() {
  cat("\n", rep("=", 60), "\n", sep = "")
  cat("📚 文献综述润色助手 (Kimi AI版)\n")
  cat(rep("=", 60), "\n\n", sep = "")
  
  # 选择学历
  academic_level <- select_academic_level()
  
  # 测试API
  test_api()
  
  cat("\n请粘贴您的文献综述内容（输入完成后，新起一行输入 END 结束）:\n\n")
  
  lines <- c()
  while (TRUE) {
    line <- readline()
    if (toupper(trimws(line)) == "END") break
    lines <- c(lines, line)
  }
  
  if (length(lines) == 0) {
    cat("❌ 未输入内容\n")
    return()
  }
  
  text <- paste(lines, collapse = "\n")
  result <- generate_full_report(text, academic_level)
  
  cat("\n", rep("=", 60), "\n", sep = "")
  cat("📝 完成！润色结果已保存到当前文件夹。\n")
  cat(rep("=", 60), "\n", sep = "")
}

# 仅分析模式（不调用API）
run_analysis_only <- function() {
  cat("\n", rep("=", 60), "\n", sep = "")
  cat("📚 文献综述分析模式（仅分析，不润色）\n")
  cat(rep("=", 60), "\n\n", sep = "")
  
  academic_level <- select_academic_level()
  
  cat("\n请粘贴您的文献综述内容（输入完成后，新起一行输入 END 结束）:\n\n")
  
  lines <- c()
  while (TRUE) {
    line <- readline()
    if (toupper(trimws(line)) == "END") break
    lines <- c(lines, line)
  }
  
  if (length(lines) == 0) {
    cat("❌ 未输入内容\n")
    return()
  }
  
  text <- paste(lines, collapse = "\n")
  analysis <- analyze_review(text, academic_level)
  
  cat("\n", rep("=", 60), "\n", sep = "")
  cat("📊 分析报告\n")
  cat(rep("=", 60), "\n", sep = "")
  
  cat(sprintf("\n学术水平: %s\n", academic_level))
  cat(sprintf("字数: %d字\n", analysis$length))
  cat(sprintf("引用密度: %.1f次/100字\n", analysis$citation_density))
  cat(sprintf("批判性评分: %d/10\n", analysis$critical_score))
  
  cat("\n📋 结构检查：\n")
  if (length(analysis$missing) > 0) {
    cat(sprintf("   ❌ 缺失: %s\n", paste(analysis$missing, collapse = ", ")))
  } else {
    cat("   ✅ 结构完整\n")
  }
  
  if (length(analysis$suggestions) > 0) {
    cat("\n💡 改进建议：\n")
    for (s in analysis$suggestions) {
      cat(sprintf("   %s\n", s))
    }
  }
  
  cat("\n", rep("=", 60), "\n", sep = "")
}

# 主函数
main <- function() {
  cat("\n请选择运行模式：\n")
  cat("1. 完整AI润色模式（推荐）\n")
  cat("2. 仅分析模式（不调用API）\n")
  cat("3. 测试API连接\n")
  cat("4. 退出\n")
  
  choice <- readline(prompt = "\n请输入 (1/2/3/4): ")
  
  if (choice == "1") {
    run_interactive()
  } else if (choice == "2") {
    run_analysis_only()
  } else if (choice == "3") {
    test_api()
  } else {
    cat("👋 再见！\n")
  }
}

# 运行
main()