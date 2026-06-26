// 病历生成器 - 核心脚本
// 这个脚本生成规范的入院记录

const fs = require('fs');
const path = require('path');

class MedicalRecordGenerator {
  constructor() {
    this.template = this.loadTemplate();
  }

  loadTemplate() {
    // 基本的病历模板
    return {
      hospital: "全科医疗科",
      ward: "01",
      recordNumber: this.generateRecordNumber(),
      basicInfo: {
        name: "待填写",
        gender: "待填写",
        age: "待填写",
        maritalStatus: "未婚",
        ethnicity: "汉族",
        birthplace: "待填写",
        occupation: "待填写"
      },
      admissionTime: new Date().toISOString().split('T')[0] + " " + new Date().toLocaleTimeString('zh-CN'),
      recordTime: new Date().toISOString().split('T')[0] + " " + new Date().toLocaleTimeString('zh-CN'),
      chiefComplaint: "待填写",
      historyOfPresentIllness: "待填写",
      pastHistory: "既往体健；否认慢性病史、传染病史、手术外伤史、输血史；否认食物药物过敏史。",
      personalHistory: "生于待填写，无长期外地居住史；无吸烟、饮酒等不良嗜好；否认工业毒物、粉尘、放射性物质接触史。",
      maritalHistory: "待填写",
      familyHistory: "否认家族性、遗传性疾病史。",
      physicalExamination: this.getDefaultPhysicalExam(),
      auxiliaryExamination: "暂缺",
      preliminaryDiagnosis: "待填写"
    };
  }

  generateRecordNumber() {
    const date = new Date();
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const random = Math.floor(Math.random() * 10000).toString().padStart(4, '0');
    return `${year}${month}${day}${random}`;
  }

  getDefaultPhysicalExam() {
    return {
      vitalSigns: {
        temperature: "36.5℃",
        pulse: "75次/分",
        respiration: "18次/分",
        bloodPressure: "120/80mmHg"
      },
      generalCondition: "发育正常，营养良好，神志清楚，体位自主，查体合作。",
      skinMucosa: "颜色正常，温度正常，湿度正常，无皮疹、出血点、黄疸等。",
      lymphNodes: "全身浅表淋巴结无肿大。",
      head: "头颅无畸形，眼睑无水肿，结膜无充血，巩膜无黄染，瞳孔等大等圆，对光反射灵敏。",
      neck: "无抵抗感，气管居中，甲状腺无肿大，颈静脉无怒张。",
      chest: "胸廓对称，呼吸动度对称，无压痛。",
      lungs: "呼吸音清，未闻及干湿性啰音。",
      heart: "心率75次/分，心律齐，无杂音。",
      abdomen: "平坦，柔软，无压痛、反跳痛，肝脾肋下未触及。",
      spineLimbs: "无畸形，活动度正常。",
      nervousSystem: "生理反射存在，病理反射未引出。"
    };
  }

  generateRecord(data) {
    // 更新模板数据
    const record = { ...this.template };
    
    // 填充基本信息
    if (data.name) record.basicInfo.name = data.name;
    if (data.gender) record.basicInfo.gender = data.gender;
    if (data.age) record.basicInfo.age = data.age;
    if (data.maritalStatus) record.basicInfo.maritalStatus = data.maritalStatus;
    if (data.occupation) record.basicInfo.occupation = data.occupation;
    if (data.birthplace) record.basicInfo.birthplace = data.birthplace;
    
    // 填充主诉和诊断
    if (data.chiefComplaint) record.chiefComplaint = data.chiefComplaint;
    if (data.historyOfPresentIllness) record.historyOfPresentIllness = data.historyOfPresentIllness;
    if (data.preliminaryDiagnosis) record.preliminaryDiagnosis = data.preliminaryDiagnosis;
    
    // 生成格式化的病历文本
    return this.formatRecord(record);
  }

  formatRecord(record) {
    const physicalExam = record.physicalExamination;
    
    return `**入院记录**

**科室**：${record.hospital}
**病房**：${record.ward}
**病案号**：${record.recordNumber}

**基本信息**
姓名：${record.basicInfo.name}
性别：${record.basicInfo.gender}
年龄：${record.basicInfo.age}
婚姻状况：${record.basicInfo.maritalStatus}
民族：${record.basicInfo.ethnicity}
出生地：${record.basicInfo.birthplace}
职业：${record.basicInfo.occupation}
入院时间：${record.admissionTime}
记录时间：${record.recordTime}
病史陈述者：患者 (可靠程度：可靠)

**主诉**：${record.chiefComplaint}

**现病史**：${record.historyOfPresentIllness}

**既往史**：${record.pastHistory}

**个人史**：${record.personalHistory}

**婚育史**：${record.maritalHistory}

**家族史**：${record.familyHistory}

**体格检查**
生命体征：T: ${physicalExam.vitalSigns.temperature}, P: ${physicalExam.vitalSigns.pulse}, R: ${physicalExam.vitalSigns.respiration}, BP: ${physicalExam.vitalSigns.bloodPressure}
一般情况：${physicalExam.generalCondition}
皮肤黏膜：${physicalExam.skinMucosa}
全身浅表淋巴结：${physicalExam.lymphNodes}
头部及其器官：${physicalExam.head}
颈部：${physicalExam.neck}
胸部：${physicalExam.chest}
肺部：${physicalExam.lungs}
心脏：${physicalExam.heart}
腹部：${physicalExam.abdomen}
脊柱四肢：${physicalExam.spineLimbs}
神经系统：${physicalExam.nervousSystem}

**辅助检查**：${record.auxiliaryExamination}

**初步诊断**：
${record.preliminaryDiagnosis}`;
  }

  // 保存病历到文件
  saveToFile(recordText, filename = null) {
    if (!filename) {
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
      filename = `medical-record-${timestamp}.md`;
    }
    
    const filepath = path.join(process.cwd(), filename);
    fs.writeFileSync(filepath, recordText, 'utf8');
    return filepath;
  }
}

// 导出模块
if (typeof module !== 'undefined' && module.exports) {
  module.exports = MedicalRecordGenerator;
}

// 如果直接运行，显示使用说明
if (require.main === module) {
  console.log('病历生成器脚本');
  console.log('使用方法：');
  console.log('1. const generator = new MedicalRecordGenerator();');
  console.log('2. const record = generator.generateRecord(data);');
  console.log('3. generator.saveToFile(record);');
}