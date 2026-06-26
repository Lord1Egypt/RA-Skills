/**
 * MS-PPT-Style v1.0.0
 * Morgan Stanley Classic PPT Style Generator
 * 
 * Usage:
 *   const msPPT = require('./MS-PPT-Skill');
 *   const pres = msPPT.createPresentation();
 *   msPPT.addCover(pres, "Title", "中文标题");
 *   msPPT.addContentPage(pres, "Section", "章节", [...]);
 *   pres.writeFile({ fileName: "output.pptx" });
 */

const pptxgen = require("pptxgenjs");

// Morgan Stanley Color Palette
const COLORS = {
  BLUE: "003087",
  LIGHT_BLUE: "1E5AA8",
  GOLD: "C9A227",
  DARK: "1A1A2E",
  WHITE: "FFFFFF",
  GRAY: "6B7280",
  LIGHT_GRAY: "F3F4F6",
  CHART: ["003087", "1E5AA8", "3B82F6", "60A5FA", "93C5FD", "C9A227", "D4AF37", "E5E7EB"]
};

/**
 * Create a new presentation with MS style defaults
 */
function createPresentation() {
  let pres = new pptxgen();
  pres.layout = 'LAYOUT_16x9';
  pres.author = 'Morgan Stanley Research';
  return pres;
}

/**
 * Add a cover slide with gradient background
 */
function addCover(pres, titleEn, titleCn, subtitle = "Research Report | 研究报告", date = "") {
  let slide = pres.addSlide();

  // Gradient background layers
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 5.625,
    fill: { color: "0A1628" }
  });
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 5.625,
    fill: { color: "1A2744", transparency: 60 }
  });

  // Gold top line
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 0.04,
    fill: { color: COLORS.GOLD }
  });

  // English title (centered)
  slide.addText(titleEn, {
    x: 0.5, y: 1.8, w: 9, h: 0.8,
    fontSize: 46, fontFace: "Arial", color: COLORS.WHITE,
    bold: true, align: "center"
  });

  // Chinese subtitle (gold, centered)
  slide.addText(titleCn, {
    x: 0.5, y: 2.7, w: 9, h: 0.5,
    fontSize: 26, fontFace: "Arial", color: COLORS.GOLD,
    align: "center"
  });

  // Gold accent line
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 4.25, y: 3.4, w: 1.5, h: 0.02,
    fill: { color: COLORS.GOLD }
  });

  // Bottom info
  const bottomText = date ? `${subtitle} · ${date}` : subtitle;
  slide.addText(bottomText, {
    x: 0.5, y: 4.8, w: 9, h: 0.25,
    fontSize: 10, fontFace: "Arial", color: "9CA3AF",
    align: "center"
  });

  return slide;
}

/**
 * Add a content page with blue header bar
 */
function addContentPage(pres, titleEn, titleCn, contentItems = []) {
  let slide = pres.addSlide();
  slide.background = { color: COLORS.WHITE };

  // Blue header bar
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 0.8,
    fill: { color: COLORS.BLUE }
  });

  // Bilingual title
  slide.addText(`${titleEn}  ${titleCn}`, {
    x: 0.5, y: 0.18, w: 8, h: 0.45,
    fontSize: 22, fontFace: "Arial", color: COLORS.WHITE,
    bold: true
  });

  // Add content items
  contentItems.forEach((item, i) => {
    const yPos = 1.2 + i * 0.8;
    
    if (typeof item === 'string') {
      slide.addText(item, {
        x: 0.5, y: yPos, w: 9, h: 0.6,
        fontSize: 12, fontFace: "Arial", color: COLORS.DARK
      });
    } else if (item.type === 'bullet') {
      slide.addShape(pres.shapes.OVAL, {
        x: 0.5, y: yPos + 0.05, w: 0.1, h: 0.1,
        fill: { color: COLORS.GOLD }
      });
      slide.addText(item.en, {
        x: 0.75, y: yPos, w: 8.7, h: 0.25,
        fontSize: 12, fontFace: "Arial", color: COLORS.DARK
      });
      if (item.cn) {
        slide.addText(item.cn, {
          x: 0.75, y: yPos + 0.25, w: 8.7, h: 0.2,
          fontSize: 10, fontFace: "Arial", color: COLORS.GRAY
        });
      }
    }
  });

  return slide;
}

/**
 * Add a metric card (3-column layout)
 */
function addMetricsPage(pres, titleEn, titleCn, metrics) {
  let slide = pres.addSlide();
  slide.background = { color: COLORS.WHITE };

  // Blue header bar
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 0.8,
    fill: { color: COLORS.BLUE }
  });

  slide.addText(`${titleEn}  ${titleCn}`, {
    x: 0.5, y: 0.18, w: 8, h: 0.45,
    fontSize: 22, fontFace: "Arial", color: COLORS.WHITE,
    bold: true
  });

  // Metrics cards
  metrics.forEach((m, i) => {
    const xPos = 0.5 + i * 3.1;
    
    slide.addShape(pres.shapes.RECTANGLE, {
      x: xPos, y: 1.5, w: 2.8, h: 1.5,
      fill: { color: COLORS.LIGHT_GRAY }
    });
    
    slide.addText(m.labelEn || m.label, {
      x: xPos + 0.12, y: 1.6, w: 2.5, h: 0.2,
      fontSize: 10, fontFace: "Arial", color: COLORS.GRAY,
      bold: true
    });
    
    slide.addText(m.value, {
      x: xPos + 0.12, y: 1.85, w: 2.5, h: 0.5,
      fontSize: 28, fontFace: "Arial", color: COLORS.BLUE,
      bold: true
    });
    
    if (m.subEn || m.sub) {
      slide.addText(m.subEn || m.sub, {
        x: xPos + 0.12, y: 2.35, w: 2.5, h: 0.2,
        fontSize: 9, fontFace: "Arial", color: COLORS.GRAY
      });
    }
  });

  return slide;
}

/**
 * Add a pie/rose chart
 */
function addPieChart(pres, titleEn, titleCn, data) {
  let slide = pres.addSlide();
  slide.background = { color: COLORS.WHITE };

  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 0.8,
    fill: { color: COLORS.BLUE }
  });

  slide.addText(`${titleEn}  ${titleCn}`, {
    x: 0.5, y: 0.18, w: 8, h: 0.45,
    fontSize: 22, fontFace: "Arial", color: COLORS.WHITE,
    bold: true
  });

  slide.addChart(pres.charts.PIE, [{
    name: "Data",
    labels: data.map(d => d.label),
    values: data.map(d => d.value)
  }], {
    x: 0.5, y: 1.2, w: 5.5, h: 4.0,
    chartColors: data.map((d, i) => COLORS.CHART[i % COLORS.CHART.length]),
    showPercent: true,
    showLegend: true,
    legendPos: "r",
    chartArea: { fill: { color: "FFFFFF" } },
    dataLabelColor: "FFFFFF",
    dataLabelFontSize: 10
  });

  return slide;
}

/**
 * Add a radar chart
 */
function addRadarChart(pres, titleEn, titleCn, series) {
  let slide = pres.addSlide();
  slide.background = { color: COLORS.WHITE };

  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 0.8,
    fill: { color: COLORS.BLUE }
  });

  slide.addText(`${titleEn}  ${titleCn}`, {
    x: 0.5, y: 0.18, w: 8, h: 0.45,
    fontSize: 22, fontFace: "Arial", color: COLORS.WHITE,
    bold: true
  });

  const radarSeries = series.map((s, i) => ({
    name: s.name,
    labels: s.labels,
    values: s.values
  }));

  slide.addChart(pres.charts.RADAR, radarSeries, {
    x: 0.5, y: 1.2, w: 5.5, h: 4.0,
    chartColors: series.map((s, i) => COLORS.CHART[i % COLORS.CHART.length]),
    lineSize: 2,
    showLegend: true,
    legendPos: "r",
    radarStyle: "filled"
  });

  return slide;
}

/**
 * Add a stacked bar chart
 */
function addStackedBarChart(pres, titleEn, titleCn, series) {
  let slide = pres.addSlide();
  slide.background = { color: COLORS.WHITE };

  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 0.8,
    fill: { color: COLORS.BLUE }
  });

  slide.addText(`${titleEn}  ${titleCn}`, {
    x: 0.5, y: 0.18, w: 8, h: 0.45,
    fontSize: 22, fontFace: "Arial", color: COLORS.WHITE,
    bold: true
  });

  const barSeries = series.map((s, i) => ({
    name: s.name,
    labels: s.labels,
    values: s.values
  }));

  slide.addChart(pres.charts.BAR, barSeries, {
    x: 0.5, y: 1.2, w: 6.0, h: 3.8,
    barDir: "bar",
    barGrouping: "stacked",
    chartColors: series.map((s, i) => COLORS.CHART[i % COLORS.CHART.length]),
    showValue: true,
    showLegend: true,
    legendPos: "b"
  });

  return slide;
}

// Export all functions
module.exports = {
  COLORS,
  createPresentation,
  addCover,
  addContentPage,
  addMetricsPage,
  addPieChart,
  addRadarChart,
  addStackedBarChart
};
