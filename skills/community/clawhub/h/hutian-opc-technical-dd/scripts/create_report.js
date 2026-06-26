const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, 
        Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType, 
        ShadingType, PageNumber, LevelFormat } = require('docx');

const tableBorder = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const cellBorders = { top: tableBorder, bottom: tableBorder, left: tableBorder, right: tableBorder };

// 报告内容
const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 24 } } },
    paragraphStyles: [
      { id: "Title", name: "Title", basedOn: "Normal",
        run: { size: 56, bold: true, color: "000000", font: "Arial" },
        paragraph: { spacing: { before: 240, after: 120 }, alignment: AlignmentType.CENTER } },
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, color: "2E74B5", font: "Arial" },
        paragraph: { spacing: { before: 360, after: 240 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, color: "2E74B5", font: "Arial" },
        paragraph: { spacing: { before: 240, after: 180 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 26, bold: true, color: "404040", font: "Arial" },
        paragraph: { spacing: { before: 200, after: 120 }, outlineLevel: 2 } },
    ]
  },
  numbering: {
    config: [
      { reference: "bullet-list",
        levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "num-list-1",
        levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "num-list-2",
        levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    ]
  },
  sections: [{
    properties: {
      page: { margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } }
    },
    headers: {
      default: new Header({ children: [new Paragraph({ 
        alignment: AlignmentType.RIGHT,
        children: [new TextRun({ text: "天津求实智源科技有限公司技术尽调报告", size: 20, color: "808080" })]
      })] })
    },
    footers: {
      default: new Footer({ children: [new Paragraph({ 
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "第 ", size: 20 }), new TextRun({ children: [PageNumber.CURRENT], size: 20 }), new TextRun({ text: " 页", size: 20 })]
      })] })
    },
    children: [
      // 标题
      new Paragraph({ heading: HeadingLevel.TITLE, children: [new TextRun("天津求实智源科技有限公司")] }),
      new Paragraph({ heading: HeadingLevel.TITLE, children: [new TextRun("技术尽调报告")] }),
      new Paragraph({ spacing: { before: 200, after: 400 }, children: [
        new TextRun({ text: "报告日期：2025年3月12日", size: 22, color: "666666" })
      ]}),
      
      // 摘要
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("摘要与核心结论")] }),
      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("一句话结论")] }),
      new Paragraph({ spacing: { after: 200 }, shading: { fill: "E8F4FD", type: ShadingType.CLEAR }, children: [
        new TextRun({ text: "天津求实智源科技有限公司是一家具有真实技术实力和明确市场定位的NILM（Non-Intrusive Load Monitoring，非侵入式负荷监测）领域专业企业，技术根基扎实、核心背书可信，但在规模化发展和资本运作方面存在明显短板。", size: 24 })
      ]}),
      
      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("投资建议等级")] }),
      new Paragraph({ spacing: { after: 200 }, children: [
        new TextRun({ text: "谨慎推荐", size: 36, bold: true, color: "E57C23" })
      ]}),
      
      // 评估表格
      new Table({
        columnWidths: [2500, 1500, 5360],
        rows: [
          new TableRow({
            tableHeader: true,
            children: [
              new TableCell({ borders: cellBorders, width: { size: 2500, type: WidthType.DXA }, shading: { fill: "2E74B5", type: ShadingType.CLEAR }, children: [new Paragraph({ children: [new TextRun({ text: "评估维度", bold: true, color: "FFFFFF", size: 22 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1500, type: WidthType.DXA }, shading: { fill: "2E74B5", type: ShadingType.CLEAR }, children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "评分", bold: true, color: "FFFFFF", size: 22 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 5360, type: WidthType.DXA }, shading: { fill: "2E74B5", type: ShadingType.CLEAR }, children: [new Paragraph({ children: [new TextRun({ text: "核心发现", bold: true, color: "FFFFFF", size: 22 })] })] }),
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders: cellBorders, width: { size: 2500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "技术实力", size: 22 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1500, type: WidthType.DXA }, children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "8.0", bold: true, size: 22 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 5360, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "依托天津大学余贻鑫院士团队，技术国际领先", size: 22 })] })] }),
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders: cellBorders, width: { size: 2500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "商业前景", size: 22 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1500, type: WidthType.DXA }, children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "6.5", bold: true, size: 22 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 5360, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "市场真实存在，但规模化和商业模式存在挑战", size: 22 })] })] }),
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders: cellBorders, width: { size: 2500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "团队稳定性", size: 22 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1500, type: WidthType.DXA }, children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "7.0", bold: true, size: 22 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 5360, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "高校背景，技术实力强，但商业化运营能力待验证", size: 22 })] })] }),
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders: cellBorders, width: { size: 2500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "财务健康", size: 22 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1500, type: WidthType.DXA }, children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "5.0", bold: true, size: 22 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 5360, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "未融资，规模较小，盈利能力不明", size: 22 })] })] }),
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders: cellBorders, width: { size: 2500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "风险可控性", size: 22 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1500, type: WidthType.DXA }, children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "6.5", bold: true, size: 22 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 5360, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "技术风险低，市场和政策风险中等", size: 22 })] })] }),
            ]
          }),
        ]
      }),
      
      // 第一层
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("第一层：材料完整性审查")] }),
      
      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("1.1 PPT声明核实情况")] }),
      new Table({
        columnWidths: [3000, 1500, 4860],
        rows: [
          new TableRow({
            tableHeader: true,
            children: [
              new TableCell({ borders: cellBorders, width: { size: 3000, type: WidthType.DXA }, shading: { fill: "2E74B5", type: ShadingType.CLEAR }, children: [new Paragraph({ children: [new TextRun({ text: "声明内容", bold: true, color: "FFFFFF", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1500, type: WidthType.DXA }, shading: { fill: "2E74B5", type: ShadingType.CLEAR }, children: [new Paragraph({ children: [new TextRun({ text: "核查结果", bold: true, color: "FFFFFF", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 4860, type: WidthType.DXA }, shading: { fill: "2E74B5", type: ShadingType.CLEAR }, children: [new Paragraph({ children: [new TextRun({ text: "验证来源", bold: true, color: "FFFFFF", size: 20 })] })] }),
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders: cellBorders, width: { size: 3000, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "成立时间：2014年10月", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "✅ 属实", bold: true, color: "008000", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 4860, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "企查查、天眼查工商注册信息", size: 20 })] })] }),
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders: cellBorders, width: { size: 3000, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "注册资本：1000万元", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "✅ 属实", bold: true, color: "008000", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 4860, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "实缴250万元，社保人数19人", size: 20 })] })] }),
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders: cellBorders, width: { size: 3000, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "发明专利100+", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "⚠️ 部分夸大", bold: true, color: "FF8C00", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 4860, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "实际有效专利约31项（含在审）", size: 20 })] })] }),
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders: cellBorders, width: { size: 3000, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "软件著作权20+", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "✅ 属实", bold: true, color: "008000", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 4860, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "企查查显示25项软件著作权", size: 20 })] })] }),
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders: cellBorders, width: { size: 3000, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "参与制定国家标准", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "✅ 属实", bold: true, color: "008000", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 4860, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "参与QGDW 12181.2-2021企业标准", size: 20 })] })] }),
            ]
          }),
        ]
      }),
      
      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("1.2 获奖记录核查")] }),
      new Table({
        columnWidths: [3000, 1500, 4860],
        rows: [
          new TableRow({
            tableHeader: true,
            children: [
              new TableCell({ borders: cellBorders, width: { size: 3000, type: WidthType.DXA }, shading: { fill: "2E74B5", type: ShadingType.CLEAR }, children: [new Paragraph({ children: [new TextRun({ text: "奖项名称", bold: true, color: "FFFFFF", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1500, type: WidthType.DXA }, shading: { fill: "2E74B5", type: ShadingType.CLEAR }, children: [new Paragraph({ children: [new TextRun({ text: "核查结果", bold: true, color: "FFFFFF", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 4860, type: WidthType.DXA }, shading: { fill: "2E74B5", type: ShadingType.CLEAR }, children: [new Paragraph({ children: [new TextRun({ text: "详细说明", bold: true, color: "FFFFFF", size: 20 })] })] }),
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders: cellBorders, width: { size: 3000, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "天津市技术发明一等奖(2018)", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "✅ 完全属实", bold: true, color: "008000", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 4860, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "余贻鑫院士负责，天津求实智源参与，已获官方公示", size: 20 })] })] }),
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders: cellBorders, width: { size: 3000, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "中国南方电网科技进步一等奖(2018)", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "⚠️ 存疑", bold: true, color: "FF8C00", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 4860, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "搜索结果未直接找到求实智源参与的南方电网一等奖", size: 20 })] })] }),
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders: cellBorders, width: { size: 3000, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "天津市电力公司科技进步一等奖(2019)", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "⚠️ 待验证", bold: true, color: "FF8C00", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 4860, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "需进一步核实获奖项目和具体时间", size: 20 })] })] }),
            ]
          }),
        ]
      }),
      
      // 第二层
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("第二层：技术可行性验证")] }),
      
      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("2.1 NILM技术概述")] }),
      new Paragraph({ spacing: { after: 200 }, children: [
        new TextRun({ text: "非侵入式负荷监测（NILM）技术：通过在电力入口安装传感器，仅分析总负荷数据即可识别各电器设备运行状态和能耗，无需在每个电器上安装传感器。该技术利用不同电器在启动、运行、停止时产生的独特电气特征（如功率变化、谐波分量、V-I轨迹等），通过模式识别和深度学习算法进行负荷分解。", size: 22 })
      ]}),
      
      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("2.2 技术水平评估")] }),
      new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun("技术鉴定结论")] }),
      new Paragraph({ spacing: { after: 200 }, shading: { fill: "FFF3E0", type: ShadingType.CLEAR }, children: [
        new TextRun({ text: "根据天津大学官网和天津市科技局公示信息：鉴定委员会一致认为项目成果总体达到了", size: 22 }),
        new TextRun({ text: "国际领先水平", bold: true, size: 22 }),
        new TextRun({ text: "。", size: 22 })
      ]}),
      
      new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun("关键技术突破")] }),
      new Paragraph({ numbering: { reference: "num-list-1", level: 0 }, children: [new TextRun({ text: "创立了多种方法融合互补的非侵入式负荷监测方法体系", size: 22 })] }),
      new Paragraph({ numbering: { reference: "num-list-1", level: 0 }, children: [new TextRun({ text: "首创完全无监督电器自适应建模方法", size: 22 })] }),
      new Paragraph({ numbering: { reference: "num-list-1", level: 0 }, children: [new TextRun({ text: "首创云-端协同非侵入式负荷监测系统解决方案", size: 22 })] }),
      
      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("2.3 核心专利分析")] }),
      new Table({
        columnWidths: [2000, 1500, 3500, 2360],
        rows: [
          new TableRow({
            tableHeader: true,
            children: [
              new TableCell({ borders: cellBorders, width: { size: 2000, type: WidthType.DXA }, shading: { fill: "2E74B5", type: ShadingType.CLEAR }, children: [new Paragraph({ children: [new TextRun({ text: "专利类型", bold: true, color: "FFFFFF", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1500, type: WidthType.DXA }, shading: { fill: "2E74B5", type: ShadingType.CLEAR }, children: [new Paragraph({ children: [new TextRun({ text: "数量", bold: true, color: "FFFFFF", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 3500, type: WidthType.DXA }, shading: { fill: "2E74B5", type: ShadingType.CLEAR }, children: [new Paragraph({ children: [new TextRun({ text: "代表性专利", bold: true, color: "FFFFFF", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 2360, type: WidthType.DXA }, shading: { fill: "2E74B5", type: ShadingType.CLEAR }, children: [new Paragraph({ children: [new TextRun({ text: "法律状态", bold: true, color: "FFFFFF", size: 20 })] })] }),
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders: cellBorders, width: { size: 2000, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "发明专利授权", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "约15项", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 3500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "CN109490679B（窃电检测）", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 2360, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "有效", size: 20 })] })] }),
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders: cellBorders, width: { size: 2000, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "发明专利实审", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "约10项", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 3500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "CN202211260053.8", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 2360, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "审查中", size: 20 })] })] }),
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders: cellBorders, width: { size: 2000, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "软件著作权", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "25项", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 3500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "EnergyDNA系统等", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 2360, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "有效", size: 20 })] })] }),
            ]
          }),
        ]
      }),
      
      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("2.4 技术路线对比")] }),
      new Table({
        columnWidths: [2000, 2500, 2500, 2360],
        rows: [
          new TableRow({
            tableHeader: true,
            children: [
              new TableCell({ borders: cellBorders, width: { size: 2000, type: WidthType.DXA }, shading: { fill: "2E74B5", type: ShadingType.CLEAR }, children: [new Paragraph({ children: [new TextRun({ text: "企业", bold: true, color: "FFFFFF", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 2500, type: WidthType.DXA }, shading: { fill: "2E74B5", type: ShadingType.CLEAR }, children: [new Paragraph({ children: [new TextRun({ text: "技术路线", bold: true, color: "FFFFFF", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 2500, type: WidthType.DXA }, shading: { fill: "2E74B5", type: ShadingType.CLEAR }, children: [new Paragraph({ children: [new TextRun({ text: "优势", bold: true, color: "FFFFFF", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 2360, type: WidthType.DXA }, shading: { fill: "2E74B5", type: ShadingType.CLEAR }, children: [new Paragraph({ children: [new TextRun({ text: "求实智源对比", bold: true, color: "FFFFFF", size: 20 })] })] }),
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders: cellBorders, width: { size: 2000, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "威胜集团", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 2500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "AI电能表+边缘计算", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 2500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "识别准确率98.5%，上市公司", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 2360, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "规模差距大", size: 20 })] })] }),
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders: cellBorders, width: { size: 2000, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "华为数字能源", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 2500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "源网荷储一体化", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 2500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "生态优势", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 2360, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "不直接竞争", size: 20 })] })] }),
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders: cellBorders, width: { size: 2000, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "求实智源", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 2500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "云-端协同+NILM", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 2500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "无监督建模", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 2360, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "专注细分领域", size: 20 })] })] }),
            ]
          }),
        ]
      }),
      
      // 第三层
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("第三层：商业逻辑验证")] }),
      
      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("3.1 市场规模分析")] }),
      new Table({
        columnWidths: [2000, 2500, 2500, 2360],
        rows: [
          new TableRow({
            tableHeader: true,
            children: [
              new TableCell({ borders: cellBorders, width: { size: 2000, type: WidthType.DXA }, shading: { fill: "2E74B5", type: ShadingType.CLEAR }, children: [new Paragraph({ children: [new TextRun({ text: "市场", bold: true, color: "FFFFFF", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 2500, type: WidthType.DXA }, shading: { fill: "2E74B5", type: ShadingType.CLEAR }, children: [new Paragraph({ children: [new TextRun({ text: "2024年规模", bold: true, color: "FFFFFF", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 2500, type: WidthType.DXA }, shading: { fill: "2E74B5", type: ShadingType.CLEAR }, children: [new Paragraph({ children: [new TextRun({ text: "2034年预测", bold: true, color: "FFFFFF", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 2360, type: WidthType.DXA }, shading: { fill: "2E74B5", type: ShadingType.CLEAR }, children: [new Paragraph({ children: [new TextRun({ text: "CAGR", bold: true, color: "FFFFFF", size: 20 })] })] }),
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders: cellBorders, width: { size: 2000, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "全球智能电表", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 2500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "282亿美元", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 2500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "1083亿美元", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 2360, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "14.1%", size: 20 })] })] }),
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders: cellBorders, width: { size: 2000, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "中国智能电表", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 2500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "超30亿人民币", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 2500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "超50亿人民币", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 2360, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "12.8%", size: 20 })] })] }),
            ]
          }),
        ]
      }),
      
      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("3.2 10年未做大原因分析")] }),
      new Paragraph({ children: [new TextRun({ text: "核心问题：为什么成立10年仍是19人的小微企业？", bold: true, size: 24 })] }),
      new Table({
        columnWidths: [2500, 6860],
        rows: [
          new TableRow({
            tableHeader: true,
            children: [
              new TableCell({ borders: cellBorders, width: { size: 2500, type: WidthType.DXA }, shading: { fill: "2E74B5", type: ShadingType.CLEAR }, children: [new Paragraph({ children: [new TextRun({ text: "原因分析", bold: true, color: "FFFFFF", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 6860, type: WidthType.DXA }, shading: { fill: "2E74B5", type: ShadingType.CLEAR }, children: [new Paragraph({ children: [new TextRun({ text: "解释", bold: true, color: "FFFFFF", size: 20 })] })] }),
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders: cellBorders, width: { size: 2500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "市场节奏", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 6860, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "NILM市场随智能电表普及而成长，2019年后才进入快车道", size: 20 })] })] }),
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders: cellBorders, width: { size: 2500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "资本缺失", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 6860, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "未获融资，无法扩大生产和市场推广", size: 20 })] })] }),
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders: cellBorders, width: { size: 2500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "渠道依赖", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 6860, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "过度依赖国网/南网，采购周期长、账期长", size: 20 })] })] }),
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders: cellBorders, width: { size: 2500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "团队构成", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 6860, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "高校背景，商业化运营能力不足", size: 20 })] })] }),
            ]
          }),
        ]
      }),
      
      // 第四层
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("第四层：风险识别")] }),
      
      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("4.1 风险评估汇总")] }),
      new Table({
        columnWidths: [2500, 1200, 1500, 4160],
        rows: [
          new TableRow({
            tableHeader: true,
            children: [
              new TableCell({ borders: cellBorders, width: { size: 2500, type: WidthType.DXA }, shading: { fill: "2E74B5", type: ShadingType.CLEAR }, children: [new Paragraph({ children: [new TextRun({ text: "风险类别", bold: true, color: "FFFFFF", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1200, type: WidthType.DXA }, shading: { fill: "2E74B5", type: ShadingType.CLEAR }, children: [new Paragraph({ children: [new TextRun({ text: "等级", bold: true, color: "FFFFFF", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1500, type: WidthType.DXA }, shading: { fill: "2E74B5", type: ShadingType.CLEAR }, children: [new Paragraph({ children: [new TextRun({ text: "类型", bold: true, color: "FFFFFF", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 4160, type: WidthType.DXA }, shading: { fill: "2E74B5", type: ShadingType.CLEAR }, children: [new Paragraph({ children: [new TextRun({ text: "主要风险点", bold: true, color: "FFFFFF", size: 20 })] })] }),
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders: cellBorders, width: { size: 2500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "技术风险", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1200, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "中", color: "FF8C00", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "中等", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 4160, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "NILM准确率瓶颈、AI大模型替代", size: 20 })] })] }),
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders: cellBorders, width: { size: 2500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "市场风险", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1200, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "高", color: "FF0000", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "高", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 4160, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "国网/南网采购周期、政策依赖", size: 20 })] })] }),
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders: cellBorders, width: { size: 2500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "财务风险", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1200, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "高", color: "FF0000", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "高", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 4160, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "营收规模小、盈利能力不明", size: 20 })] })] }),
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders: cellBorders, width: { size: 2500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "竞争风险", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1200, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "中", color: "FF8C00", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "中等", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 4160, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "大厂入局可能性、价格战", size: 20 })] })] }),
            ]
          }),
        ]
      }),
      
      // 数据来源
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("数据信息来源汇总")] }),
      new Table({
        columnWidths: [2500, 3000, 2500, 1360],
        rows: [
          new TableRow({
            tableHeader: true,
            children: [
              new TableCell({ borders: cellBorders, width: { size: 2500, type: WidthType.DXA }, shading: { fill: "2E74B5", type: ShadingType.CLEAR }, children: [new Paragraph({ children: [new TextRun({ text: "数据类别", bold: true, color: "FFFFFF", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 3000, type: WidthType.DXA }, shading: { fill: "2E74B5", type: ShadingType.CLEAR }, children: [new Paragraph({ children: [new TextRun({ text: "具体内容", bold: true, color: "FFFFFF", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 2500, type: WidthType.DXA }, shading: { fill: "2E74B5", type: ShadingType.CLEAR }, children: [new Paragraph({ children: [new TextRun({ text: "来源渠道", bold: true, color: "FFFFFF", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1360, type: WidthType.DXA }, shading: { fill: "2E74B5", type: ShadingType.CLEAR }, children: [new Paragraph({ children: [new TextRun({ text: "时间", bold: true, color: "FFFFFF", size: 20 })] })] }),
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders: cellBorders, width: { size: 2500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "工商信息", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 3000, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "注册资本、股东、经营状态", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 2500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "企查查、天眼查、启信宝", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1360, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "2025年3月", size: 20 })] })] }),
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders: cellBorders, width: { size: 2500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "专利信息", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 3000, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "31项专利明细", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 2500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "企查查、启信宝", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1360, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "2025年3月", size: 20 })] })] }),
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders: cellBorders, width: { size: 2500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "获奖信息", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 3000, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "天津市技术发明一等奖", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 2500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "天津市科技局官网", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1360, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "2025年3月", size: 20 })] })] }),
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders: cellBorders, width: { size: 2500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "市场数据", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 3000, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "智能电表行业规模", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 2500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "GM Insights、IDC报告", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1360, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "2025年3月", size: 20 })] })] }),
            ]
          }),
        ]
      }),
      
      // 人工尽调清单
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("人工尽调清单")] }),
      
      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("一、必须实地/人工验证事项")] }),
      new Table({
        columnWidths: [1000, 5500, 1500, 1360],
        rows: [
          new TableRow({
            tableHeader: true,
            children: [
              new TableCell({ borders: cellBorders, width: { size: 1000, type: WidthType.DXA }, shading: { fill: "2E74B5", type: ShadingType.CLEAR }, children: [new Paragraph({ children: [new TextRun({ text: "序号", bold: true, color: "FFFFFF", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 5500, type: WidthType.DXA }, shading: { fill: "2E74B5", type: ShadingType.CLEAR }, children: [new Paragraph({ children: [new TextRun({ text: "验证事项", bold: true, color: "FFFFFF", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1500, type: WidthType.DXA }, shading: { fill: "2E74B5", type: ShadingType.CLEAR }, children: [new Paragraph({ children: [new TextRun({ text: "优先级", bold: true, color: "FFFFFF", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1360, type: WidthType.DXA }, shading: { fill: "2E74B5", type: ShadingType.CLEAR }, children: [new Paragraph({ children: [new TextRun({ text: "说明", bold: true, color: "FFFFFF", size: 20 })] })] }),
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders: cellBorders, width: { size: 1000, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "1", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 5500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "国网检测报告原件", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "极高", bold: true, color: "FF0000", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1360, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "核实SGCM012020240024", size: 20 })] })] }),
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders: cellBorders, width: { size: 1000, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "2", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 5500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "实际营收和利润", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "极高", bold: true, color: "FF0000", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1360, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "要求提供财务报表", size: 20 })] })] }),
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders: cellBorders, width: { size: 1000, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "3", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 5500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "核心客户合同", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "高", bold: true, color: "FF8C00", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1360, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "核实南网数研院合同", size: 20 })] })] }),
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders: cellBorders, width: { size: 1000, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "4", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 5500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "团队稳定性", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "高", bold: true, color: "FF8C00", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1360, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "访谈核心人员", size: 20 })] })] }),
            ]
          }),
        ]
      }),
      
      // 综合评估
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("综合评估与投资建议")] }),
      
      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("核心优势")] }),
      new Paragraph({ numbering: { reference: "num-list-2", level: 0 }, children: [new TextRun({ text: "真实技术实力：依托天津大学余贻鑫院士团队，技术水平国际领先，有权威鉴定", size: 22 })] }),
      new Paragraph({ numbering: { reference: "num-list-2", level: 0 }, children: [new TextRun({ text: "核心资质完备：国网计量中心24项检测全部通过，参与制定行业标准", size: 22 })] }),
      new Paragraph({ numbering: { reference: "num-list-2", level: 0 }, children: [new TextRun({ text: "细分领域专注：10年深耕NILM领域，积累深厚", size: 22 })] }),
      new Paragraph({ numbering: { reference: "num-list-2", level: 0 }, children: [new TextRun({ text: "市场需求明确：智能电网、双碳目标带来持续需求", size: 22 })] }),
      
      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("主要风险")] }),
      new Paragraph({ numbering: { reference: "num-list-2", level: 0 }, children: [new TextRun({ text: "规模过小：19人参保，注册资本1000万实缴250万，规模有限", size: 22 })] }),
      new Paragraph({ numbering: { reference: "num-list-2", level: 0 }, children: [new TextRun({ text: "资本缺失：成立10年未融资，扩张能力受限", size: 22 })] }),
      new Paragraph({ numbering: { reference: "num-list-2", level: 0 }, children: [new TextRun({ text: "客户集中：过度依赖电网体系，收入稳定性风险", size: 22 })] }),
      new Paragraph({ numbering: { reference: "num-list-2", level: 0 }, children: [new TextRun({ text: "商业化能力：高校背景，市场化运营能力待验证", size: 22 })] }),
      
      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("投资建议")] }),
      new Paragraph({ spacing: { after: 200 }, shading: { fill: "E8F4FD", type: ShadingType.CLEAR }, children: [
        new TextRun({ text: "谨慎推荐", bold: true, size: 32, color: "E57C23" })
      ]}),
      
      new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun("推荐理由")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun({ text: "技术根基扎实，核心背书可信（天津市技术发明一等奖、国际领先鉴定）", size: 22 })] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun({ text: "NILM市场随智能电网建设持续成长", size: 22 })] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun({ text: "国网检测通过为进入电网供应链提供资质保障", size: 22 })] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun({ text: "比量子电池等尽调对象靠谱得多（有实体产品、有权威认证）", size: 22 })] }),
      
      new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun("谨慎理由")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun({ text: "规模过小，抵御风险能力有限", size: 22 })] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun({ text: "未融资，扩张资金来源不明", size: 22 })] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun({ text: "商业模式和盈利能力待验证", size: 22 })] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun({ text: "大厂入局可能带来竞争压力", size: 22 })] }),
      
      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("适合的投资方类型")] }),
      new Table({
        columnWidths: [2500, 1500, 5360],
        rows: [
          new TableRow({
            tableHeader: true,
            children: [
              new TableCell({ borders: cellBorders, width: { size: 2500, type: WidthType.DXA }, shading: { fill: "2E74B5", type: ShadingType.CLEAR }, children: [new Paragraph({ children: [new TextRun({ text: "投资方类型", bold: true, color: "FFFFFF", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1500, type: WidthType.DXA }, shading: { fill: "2E74B5", type: ShadingType.CLEAR }, children: [new Paragraph({ children: [new TextRun({ text: "匹配度", bold: true, color: "FFFFFF", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 5360, type: WidthType.DXA }, shading: { fill: "2E74B5", type: ShadingType.CLEAR }, children: [new Paragraph({ children: [new TextRun({ text: "说明", bold: true, color: "FFFFFF", size: 20 })] })] }),
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders: cellBorders, width: { size: 2500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "电网相关产业资本", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "高", bold: true, color: "008000", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 5360, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "协同效应明显", size: 20 })] })] }),
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders: cellBorders, width: { size: 2500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "能源电力上市公司", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "高", bold: true, color: "008000", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 5360, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "产业链整合", size: 20 })] })] }),
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders: cellBorders, width: { size: 2500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "国资背景投资机构", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "中", color: "FF8C00", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 5360, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "长期持有可考虑", size: 20 })] })] }),
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders: cellBorders, width: { size: 2500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "互联网VC/PE", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1500, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "低", color: "FF0000", size: 20 })] })] }),
              new TableCell({ borders: cellBorders, width: { size: 5360, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "与主投方向匹配度不高", size: 20 })] })] }),
            ]
          }),
        ]
      }),
      
      // 页脚
      new Paragraph({ spacing: { before: 600 }, alignment: AlignmentType.CENTER, children: [
        new TextRun({ text: "报告完成时间：2025年3月12日 | 技术尽调团队 | 内部资料", size: 18, color: "808080" })
      ]}),
    ]
  }]
});

// 保存文档
Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync('天津求实智源技术尽调报告.docx', buffer);
  console.log('DOCX报告已生成: 天津求实智源技术尽调报告.docx');
});
