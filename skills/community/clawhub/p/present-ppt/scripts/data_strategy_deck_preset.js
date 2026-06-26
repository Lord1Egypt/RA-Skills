const fs = require('fs');
const path = require('path');
const cheerio = require('cheerio');
const PptxGenJS = require('pptxgenjs');

const COLORS = {
  bg: '0A0A12',
  card: '111128',
  cardBorder: '1A1A3A',
  text: 'C8CCE0',
  bright: 'E0E3F0',
  accent: '3D5AFE',
  accent2: '7C4DFF',
  cyan: '00E5FF',
  pink: 'FF1493',
  muted: '4A4E6A',
  white: 'FFFFFF',
};

const FONT_HEAD = 'Verdana';
const FONT_BODY = 'Courier New';
const PRESET = 'data-strategy-deck';

function normalizeText(text) {
  return String(text || '')
    .replace(/ /g, ' ')
    .replace(/[\t\r\n]+/g, ' ')
    .replace(/\s+/g, ' ')
    .replace(/&amp;/g, '&')
    .replace(/&middot;/g, '·')
    .trim();
}

function ensureDir(filePath) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
}

function parseSlides(htmlPath) {
  const $ = cheerio.load(fs.readFileSync(htmlPath, 'utf8'));
  const slides = [];
  $('.slide').each((i, el) => {
    const slideEl = $(el);
    const slide = { index: i, type: null, content: {} };

    // Section label
    const sectionLabel = normalizeText(slideEl.find('.section-label').first().text());
    if (sectionLabel) slide.content.sectionLabel = sectionLabel;

    // Detect slide type based on content structure
    const hasTitleHuge = slideEl.find('.title-huge').length > 0;
    const hasStats = slideEl.find('.stats-row').length > 0;
    const hasFeatureList = slideEl.find('.feature-list').length > 0;
    const hasTwoCol = slideEl.find('.two-col').length > 0 && !slideEl.find('.two-col-3').length;
    const hasThreeCol = slideEl.find('.two-col-3').length > 0;
    const hasHouse = slideEl.find('.house-container').length > 0;
    const hasPillars = slideEl.find('.pillar-grid').length > 0;
    const hasMaturity = slideEl.find('.maturity-list').length > 0;
    const hasRoadmap = slideEl.find('.roadmap-row').length > 0;
    const hasQuoteBar = slideEl.find('.quote-bar').length > 0;

    if (hasStats) {
      slide.type = 'stats';
      slide.content.heading = normalizeText(slideEl.find('.content-heading').first().text());
      slide.content.body = normalizeText(slideEl.find('.body-text').first().text());
      slide.content.stats = [];
      slideEl.find('.stat-block').each((j, stat) => {
        const numEl = $(stat).find('.number');
        const numText = numEl.clone().children().remove().end().text().trim();
        const unit = normalizeText(numEl.find('.unit').text());
        const label = normalizeText($(stat).find('.label').text());
        slide.content.stats.push({ number: numText, unit, label });
      });
    } else if (hasFeatureList) {
      slide.type = 'agenda';
      slide.content.items = [];
      slideEl.find('.feature-row').each((j, row) => {
        slide.content.items.push({
          num: normalizeText($(row).find('.num').text()),
          title: normalizeText($(row).find('h3').text()),
          body: normalizeText($(row).find('p').text()),
        });
      });
    } else if (hasTwoCol) {
      slide.type = 'definition';
      slide.content.heading = normalizeText(slideEl.find('.content-heading').first().text());
      slide.content.body = normalizeText(slideEl.find('.body-text').first().text());
      slide.content.cols = [];
      slideEl.find('.col').each((j, col) => {
        slide.content.cols.push({
          heading: normalizeText($(col).find('h3').text()),
          body: normalizeText($(col).find('p').text()),
        });
      });
    } else if (hasHouse) {
      slide.type = 'architecture';
      slide.content.heading = normalizeText(slideEl.find('.content-heading').first().text());
      slide.content.roofLabel = normalizeText(slideEl.find('.house-roof-label').first().text());
      slide.content.floors = [];
      slideEl.find('.house-floor').each((j, floor) => {
        const floorEl = $(floor);
        slide.content.floors.push({
          name: normalizeText(floorEl.find('.floor-name').text()),
          items: floorEl.find('.floor-item').toArray().map(el => normalizeText($(el).text())),
          cls: floorEl.attr('class') || '',
        });
      });
    } else if (hasPillars) {
      slide.type = 'pillars';
      slide.content.heading = normalizeText(slideEl.find('.content-heading').first().text());
      slide.content.cards = [];
      slideEl.find('.pillar-card').each((j, card) => {
        slide.content.cards.push({
          title: normalizeText($(card).find('h3').text()),
          body: normalizeText($(card).find('p').text()),
        });
      });
    } else if (hasMaturity) {
      slide.type = 'maturity';
      slide.content.heading = normalizeText(slideEl.find('.content-heading').first().text());
      slide.content.levels = [];
      slideEl.find('.maturity-row').each((j, row) => {
        slide.content.levels.push({
          level: normalizeText($(row).find('.level').text()),
          desc: normalizeText($(row).find('.desc').text()),
        });
      });
    } else if (hasThreeCol) {
      slide.type = 'assessment';
      slide.content.heading = normalizeText(slideEl.find('.content-heading').first().text());
      slide.content.body = normalizeText(slideEl.find('.body-text').first().text());
      slide.content.cols = [];
      slideEl.find('.col').each((j, col) => {
        slide.content.cols.push({
          heading: normalizeText($(col).find('h3').text()),
          body: normalizeText($(col).find('p').text()),
        });
      });
    } else if (hasRoadmap) {
      slide.type = 'roadmap';
      slide.content.heading = normalizeText(slideEl.find('.content-heading').first().text());
      slide.content.phases = [];
      slideEl.find('.roadmap-row').each((j, row) => {
        slide.content.phases.push({
          phase: normalizeText($(row).find('.roadmap-phase').text()),
          desc: normalizeText($(row).find('.roadmap-desc').text()),
          time: normalizeText($(row).find('.roadmap-time').text()),
        });
      });
    } else if (hasQuoteBar) {
      slide.type = 'closing';
      slide.content.title = normalizeText(slideEl.find('.close-title').text());
      slide.content.subtitle = normalizeText(slideEl.find('.close-sub').text());
    } else if (hasTitleHuge) {
      slide.type = 'title';
      slide.content.title = normalizeText(slideEl.find('.title-huge').text());
      slide.content.subtitle = normalizeText(slideEl.find('.subtitle').first().text());
    } else {
      slide.type = 'generic';
      const heading = slideEl.find('.content-heading').first();
      if (heading.length) slide.content.heading = normalizeText(heading.text());
      const body = slideEl.find('.body-text').first();
      if (body.length) slide.content.body = normalizeText(body.text());
    }

    slides.push(slide);
  });
  return slides;
}

function addText(slide, text, opts = {}) {
  slide.addText(text, {
    fontFace: FONT_BODY,
    color: COLORS.text,
    margin: 0,
    valign: 'top',
    breakLine: false,
    ...opts,
  });
}

function addRoundedRect(slide, pptx, opts = {}) {
  slide.addShape(pptx.ShapeType.roundRect, {
    rectRadius: 0.08,
    fill: { color: COLORS.card },
    line: { color: COLORS.cardBorder, width: 0.8 },
    ...opts,
  });
}

function renderSlides(slides, outPath, pptx) {
  slides.forEach((slide, idx) => {
    const s = pptx.addSlide();
    s.background = { color: COLORS.bg };

    switch (slide.type) {
      case 'title':
        renderTitleSlide(s, pptx, slide.content);
        break;
      case 'stats':
        renderStatsSlide(s, pptx, slide.content);
        break;
      case 'agenda':
        renderAgendaSlide(s, pptx, slide.content);
        break;
      case 'definition':
        renderDefinitionSlide(s, pptx, slide.content);
        break;
      case 'architecture':
        renderArchitectureSlide(s, pptx, slide.content);
        break;
      case 'pillars':
        renderPillarsSlide(s, pptx, slide.content);
        break;
      case 'maturity':
        renderMaturitySlide(s, pptx, slide.content);
        break;
      case 'assessment':
        renderAssessmentSlide(s, pptx, slide.content);
        break;
      case 'roadmap':
        renderRoadmapSlide(s, pptx, slide.content);
        break;
      case 'closing':
        renderClosingSlide(s, pptx, slide.content);
        break;
      default:
        renderGenericSlide(s, pptx, slide.content);
    }

    // Page number
    addText(s, `${String(idx + 1).padStart(2, '0')} / ${String(slides.length).padStart(2, '0')}`, {
      x: 8.8, y: 7.0, w: 4.0, h: 0.25,
      fontSize: 9, color: COLORS.muted, align: 'right',
      fontFace: FONT_HEAD,
    });
  });

  ensureDir(outPath);
  return pptx.writeFile({ fileName: outPath });
}

function $label(s, pptx, text, y) {
  addText(s, text, {
    x: 0.5, y, w: 5, h: 0.25,
    fontSize: 11, color: COLORS.accent, fontFace: FONT_HEAD, bold: true,
  });
}

function $heading(s, text, y) {
  // Strip HTML artifacts from heading
  const clean = text.replace(/<\/?span[^>]*>/g, '').replace(/\s+/g, ' ').trim();
  addText(s, clean, {
    x: 0.5, y, w: 12, h: 0.55,
    fontSize: 26, color: COLORS.bright, fontFace: FONT_HEAD, bold: true,
  });
}

function $body(s, text, y) {
  addText(s, text, {
    x: 0.5, y, w: 9, h: 0.50,
    fontSize: 13, color: COLORS.muted,
  });
}

// === Slide renderers ===

function renderTitleSlide(s, pptx, c) {
  // Section label
  addText(s, c.sectionLabel, {
    x: 0.5, y: 1.5, w: 6, h: 0.3,
    fontSize: 12, color: COLORS.accent, fontFace: FONT_HEAD, bold: true,
  });
  // Big title
  addText(s, 'DATA\nSTRATEGY', {
    x: 0.5, y: 2.0, w: 10, h: 2.0,
    fontSize: 52, color: COLORS.bright, fontFace: FONT_HEAD, bold: true,
    lineSpacingMultiple: 0.92,
  });
  // Accented "STRATEGY" overlay
  addText(s, 'STRATEGY', {
    x: 0.5, y: 2.0, w: 10, h: 1.1,
    fontSize: 52, color: COLORS.accent, fontFace: FONT_HEAD, bold: true,
  });
  // Subtitle
  addText(s, c.subtitle || '', {
    x: 0.5, y: 3.8, w: 8, h: 0.35,
    fontSize: 13, color: COLORS.muted,
  });
  // Status line
  addText(s, '[  SYS.INIT // ACTIVE  ]', {
    x: 0.5, y: 6.5, w: 5, h: 0.3,
    fontSize: 9, color: COLORS.muted, fontFace: FONT_HEAD,
  });
}

function renderStatsSlide(s, pptx, c) {
  $label(s, pptx, c.sectionLabel, 0.5);
  $heading(s, c.heading, 0.9);
  $body(s, c.body, 1.55);

  (c.stats || []).forEach((stat, idx) => {
    const x = 0.5 + idx * 4.0;
    addText(s, stat.number, {
      x, y: 2.5, w: 3.5, h: 0.9,
      fontSize: 48, color: COLORS.bright, fontFace: FONT_HEAD, bold: true,
    });
    addText(s, stat.unit, {
      x: x + stat.number.length * 0.35, y: 2.5, w: 1, h: 0.5,
      fontSize: 18, color: COLORS.accent, fontFace: FONT_HEAD, bold: true,
    });
    addText(s, stat.label, {
      x, y: 3.3, w: 3.5, h: 0.35,
      fontSize: 10, color: COLORS.muted, fontFace: FONT_HEAD,
    });
  });
}

function renderAgendaSlide(s, pptx, c) {
  $label(s, pptx, c.sectionLabel, 0.5);
  addText(s, 'AGENDA', {
    x: 0.5, y: 0.9, w: 5, h: 0.55,
    fontSize: 26, color: COLORS.bright, fontFace: FONT_HEAD, bold: true,
  });

  (c.items || []).forEach((item, idx) => {
    const y = 1.7 + idx * 1.1;
    // Dividing line
    if (idx === 0) {
      s.addShape(pptx.ShapeType.line, {
        x: 0.5, y, w: 8, h: 0,
        line: { color: COLORS.cardBorder, width: 0.8 },
      });
    }
    addText(s, item.num, {
      x: 0.5, y: y + 0.08, w: 1, h: 0.4,
      fontSize: 22, color: COLORS.accent, fontFace: FONT_HEAD, bold: true,
    });
    addText(s, item.title, {
      x: 1.5, y: y + 0.08, w: 6, h: 0.25,
      fontSize: 13, color: COLORS.bright, fontFace: FONT_HEAD, bold: true,
    });
    addText(s, item.body, {
      x: 1.5, y: y + 0.35, w: 6.5, h: 0.25,
      fontSize: 10, color: COLORS.muted,
    });
    s.addShape(pptx.ShapeType.line, {
      x: 0.5, y: y + 0.85, w: 8, h: 0,
      line: { color: COLORS.cardBorder, width: 0.8 },
    });
  });
}

function renderDefinitionSlide(s, pptx, c) {
  $label(s, pptx, c.sectionLabel, 0.5);
  $heading(s, c.heading, 0.9);
  $body(s, c.body, 1.55);

  (c.cols || []).forEach((col, idx) => {
    const x = 0.5 + idx * 5.5;
    addText(s, col.heading, {
      x, y: 2.4, w: 5, h: 0.3,
      fontSize: 11, color: COLORS.cyan, fontFace: FONT_HEAD, bold: true,
    });
    addText(s, col.body, {
      x, y: 2.8, w: 5, h: 0.7,
      fontSize: 12, color: COLORS.text,
    });
  });
}

function renderArchitectureSlide(s, pptx, c) {
  $label(s, pptx, c.sectionLabel, 0.3);
  addText(s, c.heading.replace(/<\/?span[^>]*>/g, '').trim(), {
    x: 0.5, y: 0.7, w: 12, h: 0.45,
    fontSize: 22, color: COLORS.bright, fontFace: FONT_HEAD, bold: true, align: 'center',
  });

  // Roof - draw triangle using lines
  const roofLeft = 3.0, roofRight = 9.5, roofTop = 1.25, roofPeakY = 1.65, roofBaseY = 2.1;
  s.addShape(pptx.ShapeType.line, { x: roofLeft, y: roofBaseY, w: roofRight - roofLeft, h: 0, line: { color: COLORS.accent, width: 2 } });
  s.addShape(pptx.ShapeType.line, { x: (roofLeft + roofRight) / 2, y: roofPeakY, w: -(roofRight - roofLeft) / 2, h: roofBaseY - roofPeakY, line: { color: COLORS.accent, width: 1.5 } });
  s.addShape(pptx.ShapeType.line, { x: (roofLeft + roofRight) / 2, y: roofPeakY, w: (roofRight - roofLeft) / 2, h: roofBaseY - roofPeakY, line: { color: COLORS.accent, width: 1.5 } });
  // Roof fill - use a triangle shape
  s.addShape(pptx.ShapeType.triangle, {
    x: roofLeft, y: roofPeakY, w: roofRight - roofLeft, h: roofBaseY - roofPeakY,
    fill: { color: COLORS.accent, transparency: 70 },
    line: { color: COLORS.accent, width: 0 },
  });
  addText(s, 'DATA-DRIVEN OUTCOMES', {
    x: roofLeft, y: roofPeakY - 0.05, w: roofRight - roofLeft, h: roofBaseY - roofPeakY,
    fontSize: 10, color: COLORS.white, fontFace: FONT_HEAD, bold: true, align: 'center',
  });

  // Floors
  const floorNames = ['Analytics & Insights', 'Data Platform', 'Data Foundation', 'People & Culture'];
  const floorColors = [COLORS.cyan, COLORS.accent, COLORS.accent2, COLORS.pink];
  const floorItems = [
    ['BI Dashboards', 'AI / ML Models', 'Self-Service Analytics', 'Real-Time Reports'],
    ['Data Lakehouse', 'ETL / Pipelines', 'Data Catalog', 'APIs & Integration'],
    ['Data Governance', 'Data Quality', 'Security & Privacy', 'Metadata Management'],
    ['Data Literacy', 'Data-Driven Mindset', 'Cross-Functional Collaboration'],
  ];

  const startY = 2.3;
  const floorH = 0.85;

  floorNames.forEach((name, idx) => {
    const y = startY + idx * (floorH + 0.08);
    addRoundedRect(s, pptx, {
      x: 2.5, y, w: 7.5, h: floorH,
      fill: { color: floorColors[idx], transparency: 90 },
      line: { color: floorColors[idx], transparency: 80, width: 0.6 },
    });
    addText(s, name, {
      x: 2.7, y: y + 0.05, w: 7, h: 0.25,
      fontSize: 10, color: floorColors[idx], fontFace: FONT_HEAD, bold: true, align: 'center',
    });
    const items = floorItems[idx] || [];
    const itemText = items.join('    ');
    addText(s, itemText, {
      x: 2.7, y: y + 0.32, w: 7, h: 0.32,
      fontSize: 8, color: COLORS.muted, align: 'center',
    });
  });

  // Foundation bar
  addRoundedRect(s, pptx, {
    x: 2.3, y: startY + 4 * (floorH + 0.08) + 0.05, w: 8.9, h: 0.15,
    fill: { color: COLORS.accent, transparency: 80 },
    line: { color: COLORS.accent, width: 0 },
    rectRadius: 0.04,
  });
}

function renderPillarsSlide(s, pptx, c) {
  $label(s, pptx, c.sectionLabel, 0.5);
  $heading(s, c.heading, 0.9);

  const cardColors = [COLORS.accent, COLORS.cyan, COLORS.pink, COLORS.accent2];
  (c.cards || []).forEach((card, idx) => {
    const x = 0.5 + (idx % 2) * 4.5;
    const y = 1.7 + Math.floor(idx / 2) * 2.1;
    addRoundedRect(s, pptx, {
      x, y, w: 4.2, h: 1.8,
      fill: { color: COLORS.card },
      line: { color: cardColors[idx], transparency: 80, width: 0.8 },
    });
    // Accent top line
    s.addShape(pptx.ShapeType.line, {
      x, y, w: 4.2, h: 0,
      line: { color: cardColors[idx], width: 2.5 },
    });
    addText(s, card.title, {
      x: x + 0.25, y: y + 0.25, w: 3.7, h: 0.35,
      fontSize: 15, color: COLORS.bright, fontFace: FONT_HEAD, bold: true,
    });
    addText(s, card.body, {
      x: x + 0.25, y: y + 0.7, w: 3.7, h: 0.8,
      fontSize: 11, color: COLORS.muted,
    });
  });
}

function renderMaturitySlide(s, pptx, c) {
  $label(s, pptx, c.sectionLabel, 0.5);
  $heading(s, c.heading, 0.9);

  (c.levels || []).forEach((level, idx) => {
    const y = 1.7 + idx * 0.95;
    // Line separator
    if (idx === 0) {
      s.addShape(pptx.ShapeType.line, {
        x: 0.5, y, w: 9, h: 0,
        line: { color: COLORS.cardBorder, width: 0.8 },
      });
    }
    addText(s, level.level, {
      x: 0.5, y: y + 0.08, w: 1.8, h: 0.3,
      fontSize: 10, color: COLORS.accent, fontFace: FONT_HEAD, bold: true,
    });
    addText(s, level.desc, {
      x: 2.4, y: y + 0.08, w: 7.5, h: 0.35,
      fontSize: 11, color: COLORS.text,
    });
    s.addShape(pptx.ShapeType.line, {
      x: 0.5, y: y + 0.7, w: 9, h: 0,
      line: { color: COLORS.cardBorder, width: 0.8 },
    });
  });
}

function renderAssessmentSlide(s, pptx, c) {
  $label(s, pptx, c.sectionLabel, 0.5);
  $heading(s, c.heading, 0.9);
  $body(s, c.body, 1.55);

  (c.cols || []).forEach((col, idx) => {
    const x = 0.5 + idx * 3.2;
    addText(s, col.heading, {
      x, y: 2.4, w: 3, h: 0.3,
      fontSize: 10, color: COLORS.cyan, fontFace: FONT_HEAD, bold: true,
    });
    addText(s, col.body, {
      x, y: 2.75, w: 2.9, h: 1.2,
      fontSize: 11, color: COLORS.text,
    });
  });
}

function renderRoadmapSlide(s, pptx, c) {
  $label(s, pptx, c.sectionLabel, 0.5);
  $heading(s, c.heading, 0.9);

  const phaseColors = [COLORS.accent, COLORS.accent2, COLORS.pink];
  (c.phases || []).forEach((phase, idx) => {
    const y = 1.7 + idx * 1.6;
    const color = phaseColors[idx] || COLORS.accent;
    addRoundedRect(s, pptx, {
      x: 0.5, y, w: 11.5, h: 1.3,
      fill: { color: COLORS.card },
      line: { color: color, transparency: 80, width: 0.8 },
    });
    addText(s, phase.phase, {
      x: 0.8, y: y + 0.15, w: 2, h: 0.3,
      fontSize: 11, color, fontFace: FONT_HEAD, bold: true,
    });
    addText(s, phase.desc, {
      x: 2.8, y: y + 0.15, w: 6.5, h: 0.6,
      fontSize: 11, color: COLORS.text,
    });
    addText(s, phase.time, {
      x: 9.8, y: y + 0.15, w: 2, h: 0.3,
      fontSize: 10, color: COLORS.cyan, fontFace: FONT_HEAD, align: 'right',
    });
  });
}

function renderClosingSlide(s, pptx, c) {
  // Accent bar
  s.addShape(pptx.ShapeType.line, {
    x: 0.5, y: 1.8, w: 2.5, h: 0,
    line: { color: COLORS.accent, width: 3 },
  });
  // Title
  addText(s, 'Build Your', {
    x: 0.5, y: 2.1, w: 8, h: 0.7,
    fontSize: 36, color: COLORS.bright, fontFace: FONT_HEAD, bold: true,
  });
  addText(s, 'House', {
    x: 0.5, y: 2.7, w: 8, h: 0.7,
    fontSize: 36, color: COLORS.accent, fontFace: FONT_HEAD, bold: true,
  });
  addText(s, c.subtitle || '', {
    x: 0.5, y: 3.6, w: 8, h: 0.4,
    fontSize: 13, color: COLORS.muted,
  });
  // Cursor
  addText(s, 'END TRANSMISSION_', {
    x: 0.5, y: 6.5, w: 5, h: 0.3,
    fontSize: 10, color: COLORS.muted, fontFace: FONT_HEAD,
  });
}

function renderGenericSlide(s, pptx, c) {
  if (c.sectionLabel) $label(s, pptx, c.sectionLabel, 0.5);
  if (c.heading) $heading(s, c.heading, 0.9);
  if (c.body) $body(s, c.body, 1.55);
}

// Main export
function extractDataStrategyDeck(htmlPath) {
  return {
    preset: PRESET,
    slides: parseSlides(htmlPath),
  };
}

function renderDataStrategyDeck(model, outPath, pptx) {
  return renderSlides(model.slides, outPath, pptx);
}

module.exports = {
  PRESET,
  extractDataStrategyDeck,
  renderDataStrategyDeck,
};
