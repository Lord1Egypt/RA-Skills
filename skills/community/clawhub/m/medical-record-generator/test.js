// 测试病历生成器
const MedicalRecordGenerator = require('./scripts/generate_record.js');
const generator = new MedicalRecordGenerator();

// 测试数据 - 基于用户提供的病例
const testData = {
  name: "待填写",
  gender: "女性",
  age: "70岁",
  maritalStatus: "已婚",
  occupation: "退休",
  birthplace: "待填写",
  chiefComplaint: "反复咳嗽、喘息10年，加重3天",
  historyOfPresentIllness: "患者于10年前无明显诱因出现反复咳嗽、喘息，症状呈慢性进行性加重。3天前因受凉后症状明显加重，咳嗽加剧，喘息明显，活动后气促。发病以来，精神差，睡眠差，食欲减退，大小便正常，体重无明显变化。",
  preliminaryDiagnosis: "慢性阻塞性肺疾病急性加重"
};

console.log("=== 测试病历生成器 ===");
console.log("测试数据：");
console.log(JSON.stringify(testData, null, 2));
console.log("\n=== 生成的病历 ===");

// 生成病历
const record = generator.generateRecord(testData);
console.log(record);

// 保存到文件
const filepath = generator.saveToFile(record, "test-medical-record.md");
console.log(`\n病历已保存到: ${filepath}`);

// 验证文件是否存在
const fs = require('fs');
if (fs.existsSync(filepath)) {
  console.log("✅ 测试成功：病历文件已创建");
  console.log(`文件大小：${fs.statSync(filepath).size} 字节`);
} else {
  console.log("❌ 测试失败：病历文件未创建");
}