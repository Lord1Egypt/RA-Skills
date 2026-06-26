#!/usr/bin/env node

const fs = require("fs");
const path = require("path");
const { Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell, WidthType, AlignmentType } = require("docx");

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, "utf8"));
}

function ensureDir(dirPath) {
  fs.mkdirSync(dirPath, { recursive: true });
}

function safe(value, fallback = "") {
  return value == null ? fallback : String(value);
}

function csvEscape(value) {
  const str = safe(value);
  if (str.includes(",") || str.includes("\"") || str.includes("\n")) return `"${str.replace(/"/g, "\"\"")}"`;
  return str;
}

function detectIssues(employee, meta) {
  const issues = [];
  if (!employee.bank_account) issues.push({ level: "high", code: "missing_bank_account", message: "缺少工资银行卡信息" });
  if (!employee.id_number) issues.push({ level: "high", code: "missing_id_number", message: "缺少身份证号，存在个税申报风险" });
  if (employee.employment_status === "left" && (employee.tax_declaration || employee.social_insurance_declaration || employee.housing_fund_declaration)) {
    issues.push({ level: "high", code: "left_employee_still_declared", message: "离职员工仍在本月申报名单中" });
  }
  if (employee.legal_entity !== meta.legal_entity) {
    issues.push({ level: "high", code: "wrong_legal_entity", message: "申报主体与本次发薪主体不一致" });
  }
  if (employee.city !== "上海" && employee.social_insurance_declaration) {
    issues.push({ level: "medium", code: "cross_city_check", message: "缴纳城市与当前申报口径可能不一致，需复核" });
  }
  if (employee.housing_fund_declaration && Number(employee.housing_fund_base || 0) <= 0) {
    issues.push({ level: "high", code: "missing_housing_fund_base", message: "公积金需申报但缴存基数为 0" });
  }
  if (employee.social_insurance_declaration && Number(employee.social_base || 0) <= 0) {
    issues.push({ level: "high", code: "missing_social_base", message: "社保需申报但缴费基数为 0" });
  }
  if (Number(employee.social_base || 0) > Number(employee.salary_taxable_income || 0) * 1.15 && Number(employee.salary_taxable_income || 0) > 0) {
    issues.push({ level: "medium", code: "social_base_high", message: "社保基数明显高于当前应税收入，建议复核口径" });
  }
  if (Number(employee.special_additional_deduction || 0) === 0 && Number(employee.salary_taxable_income || 0) > 15000) {
    issues.push({ level: "low", code: "deduction_zero", message: "专项附加扣除为 0，可确认员工是否已填报" });
  }
  if (!employee.social_insurance_declaration && employee.housing_fund_declaration) {
    issues.push({ level: "medium", code: "fund_without_social", message: "公积金申报存在，但社保未申报，需确认人员缴纳状态" });
  }
  return issues;
}

function summarize(all) {
  const counts = { high: 0, medium: 0, low: 0 };
  all.forEach((x) => x.issues.forEach((issue) => { counts[issue.level] += 1; }));
  return counts;
}

function buildInternalMessage(highRiskEmployees) {
  if (!highRiskEmployees.length) return "本次申报前检查未发现高风险错误，可继续进入复核与申报环节。";
  return `本次申报前检查发现 ${highRiskEmployees.length} 名高风险人员，请优先补齐缺失字段、复核离职人员状态和申报主体/缴纳口径，再进入正式申报。`;
}

async function writeDocx(filePath, title, sections) {
  const doc = new Document({
    sections: [{ children: [new Paragraph({ text: title, heading: HeadingLevel.TITLE, alignment: AlignmentType.CENTER }), ...sections] }]
  });
  fs.writeFileSync(filePath, await Packer.toBuffer(doc));
}

function para(text, opts = {}) {
  return new Paragraph({ text, heading: opts.heading, spacing: { after: 160 } });
}

function bullet(text) {
  return new Paragraph({ text, bullet: { level: 0 }, spacing: { after: 120 } });
}

function keyValueTable(rows) {
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    rows: rows.map(([k, v]) => new TableRow({
      children: [
        new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: k, bold: true })] })] }),
        new TableCell({ children: [new Paragraph(safe(v))] })
      ]
    }))
  });
}

async function main() {
  const inputPath = process.argv[2];
  const outDir = process.argv[3];
  if (!inputPath || !outDir) {
    console.error("Usage: node scripts/generate_payroll_precheck_packet.js <input.json> <output-dir>");
    process.exit(1);
  }

  const payload = readJson(inputPath);
  ensureDir(outDir);

  const analyzed = payload.employees.map((employee) => ({ employee, issues: detectIssues(employee, payload.meta) }));
  const counts = summarize(analyzed);
  const highRiskEmployees = analyzed.filter((x) => x.issues.some((issue) => issue.level === "high"));
  const missingFields = analyzed.flatMap((x) =>
    x.issues
      .filter((issue) => issue.code.startsWith("missing"))
      .map((issue) => ({ employee_name: x.employee.employee_name, field_issue: issue.message }))
  );

  const reportPath = path.join(outDir, "payroll-filing-precheck-report.docx");
  const messagePath = path.join(outDir, "internal-risk-message.docx");
  const trackerPath = path.join(outDir, "payroll-filing-precheck.csv");
  const jsonPath = path.join(outDir, "payroll-filing-precheck-output.json");

  await writeDocx(reportPath, "薪酬申报前检查报告", [
    para("一、检查范围", { heading: HeadingLevel.HEADING_1 }),
    keyValueTable([
      ["法人主体", payload.meta.legal_entity],
      ["工资所属月份", payload.meta.payroll_month],
      ["检查人数", payload.employees.length],
      ["准备人", payload.meta.prepared_by]
    ]),
    para("二、风险概览", { heading: HeadingLevel.HEADING_1 }),
    bullet(`高风险问题数：${counts.high}`),
    bullet(`中风险问题数：${counts.medium}`),
    bullet(`低风险问题数：${counts.low}`),
    bullet(`高风险人员数：${highRiskEmployees.length}`),
    para("三、优先处理人员", { heading: HeadingLevel.HEADING_1 }),
    ...highRiskEmployees.flatMap((item) => [
      para(`${item.employee.employee_name}（${item.employee.employee_id}）`, { heading: HeadingLevel.HEADING_2 }),
      ...item.issues.filter((issue) => issue.level === "high").map((issue) => bullet(issue.message))
    ]),
    para("四、建议下一步", { heading: HeadingLevel.HEADING_1 }),
    bullet("先补齐缺失身份证号、银行卡号和基数字段。"),
    bullet("先剔除离职但仍在申报名单中的人员。"),
    bullet("复核跨主体、跨城市、社保与公积金申报口径不一致的人员。"),
    bullet("高风险问题关闭后，再进入个税、社保、公积金正式申报。")
  ]);

  await writeDocx(messagePath, "内部风险说明稿", [
    para("建议发送对象：薪酬、HRBP、财务或共享服务同事", { heading: HeadingLevel.HEADING_1 }),
    para(buildInternalMessage(highRiskEmployees)),
    para("建议补充说明：", { heading: HeadingLevel.HEADING_1 }),
    bullet("高风险项请优先在申报前完成修正。"),
    bullet("跨主体或跨城市问题请同步确认当月申报口径。"),
    bullet("如需更正上期申报，请单独标记处理，不与本期正常申报混淆。")
  ]);

  const header = ["employee_name", "employee_id", "risk_level", "issue_message", "next_action"];
  const rows = analyzed.flatMap((item) =>
    item.issues.map((issue) => [
      item.employee.employee_name,
      item.employee.employee_id,
      issue.level,
      issue.message,
      issue.level === "high" ? "优先处理并复核后再申报" : "复核后决定是否继续申报"
    ])
  );
  fs.writeFileSync(
    trackerPath,
    `${header.join(",")}\n${rows.map((row) => row.map(csvEscape).join(",")).join("\n")}\n`,
    "utf8"
  );

  fs.writeFileSync(
    jsonPath,
    JSON.stringify({
      normalized_data: {
        meta: payload.meta,
        employees: payload.employees,
        issue_count: counts
      },
      missing_information: missingFields,
      risk_summary: buildInternalMessage(highRiskEmployees),
      priority_issues: highRiskEmployees.map((item) => ({
        employee_name: item.employee.employee_name,
        issues: item.issues.filter((issue) => issue.level === "high").map((issue) => issue.message)
      })),
      next_action: "先处理高风险人员和缺失字段，再进入正式申报。",
      message_draft: buildInternalMessage(highRiskEmployees),
      record_update: {
        payroll_month: payload.meta.payroll_month,
        legal_entity: payload.meta.legal_entity,
        high_risk_count: highRiskEmployees.length
      },
      compliance_warning_if_any: highRiskEmployees.length ? ["存在高风险申报问题，建议先修正后申报。"] : []
    }, null, 2),
    "utf8"
  );

  console.log(JSON.stringify({
    ok: true,
    files: {
      report: reportPath,
      message: messagePath,
      tracker: trackerPath,
      json: jsonPath
    }
  }, null, 2));
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
