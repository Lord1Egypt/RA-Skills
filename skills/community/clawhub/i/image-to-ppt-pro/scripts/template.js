#!/usr/bin/env node
/**
 * ppt-replicator example script
 * This file is a reference template for replicating PPT from screenshots
 * 
 * Usage:
 *   NODE_PATH=/home/claude/.npm-global/lib/node_modules node create_slide.js
 * 
 * In actual use, Claude generates corresponding scripts based on specific image content.
 * This file only shows common patterns for reference.
 */

const pptxgen = require("pptxgenjs");
let pres = new pptxgen();
pres.layout = 'LAYOUT_16x9'; // 10" × 5.625"
let slide = pres.addSlide();

// ===== Background =====
slide.background = { color: "FFFFFF" };

// ===== Top header (dark red) =====
slide.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 0.65,
  fill: { color: "8B1A1A" },
  line: { color: "8B1A1A" }
});
slide.addText("Slide Title", {
  x: 0.25, y: 0, w: 7.5, h: 0.65,
  fontSize: 22, bold: true, color: "FFFFFF",
  fontFace: "Microsoft YaHei", valign: "middle", margin: 0
});
// Top right logo/organization name
slide.addText("Organization Name", {
  x: 8.0, y: 0, w: 1.9, h: 0.65,
  fontSize: 11, bold: true, color: "FFFFFF",
  fontFace: "Microsoft YaHei", align: "right", valign: "middle", margin: 5
});

// ===== Main content: Flowchart example =====

// Flowchart background area
slide.addShape(pres.shapes.RECTANGLE, {
  x: 0.2, y: 0.75, w: 5.2, h: 4.5,
  fill: { color: "F5F5F5" },
  line: { color: "E0E0E0", width: 1 }
});

// Node 1: Top (gray)
slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 1.4, y: 0.95, w: 2.4, h: 0.42,
  fill: { color: "D9D9D9" }, line: { color: "AAAAAA", width: 1 }, rectRadius: 0.05
});
slide.addText("Start Node", {
  x: 1.4, y: 0.95, w: 2.4, h: 0.42,
  fontSize: 11, color: "333333", fontFace: "Microsoft YaHei",
  align: "center", valign: "middle", margin: 0
});

// Connector (vertical line)
slide.addShape(pres.shapes.LINE, {
  x: 2.6, y: 1.37, w: 0, h: 0.25,
  line: { color: "888888", width: 1.5 }
});

// Node 2 (purple)
slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 0.55, y: 1.62, w: 4.1, h: 0.55,
  fill: { color: "E8E0F0" }, line: { color: "C0A8D8", width: 1 }, rectRadius: 0.05
});
slide.addText([
  { text: "Processing Node Title", options: { breakLine: true } },
  { text: "Supplementary description, can be smaller", options: { fontSize: 7.5, color: "666666" } }
], {
  x: 0.55, y: 1.62, w: 4.1, h: 0.55,
  fontSize: 10, color: "444444", fontFace: "Microsoft YaHei",
  align: "center", valign: "middle", margin: 0
});

// ===== Right description text area =====
slide.addText("File Structure Description Title:", {
  x: 5.55, y: 0.85, w: 4.2, h: 0.4,
  fontSize: 13, bold: true, color: "333333", fontFace: "Microsoft YaHei"
});

// Link style text
slide.addText("filename.md", {
  x: 5.55, y: 1.5, w: 4.2, h: 0.3,
  fontSize: 12, color: "1155CC", fontFace: "Microsoft YaHei",
  underline: { style: "sng" }
});
slide.addText("is file description text,", {
  x: 5.55, y: 1.78, w: 4.2, h: 0.3,
  fontSize: 12, color: "333333", fontFace: "Microsoft YaHei"
});

// Mixed style (multiple colors in same line)
slide.addText([
  { text: "fileA.md", options: { color: "1155CC", underline: { style: "sng" } } },
  { text: " and ", options: { color: "333333" } },
  { text: "fileB.md", options: { color: "1155CC", underline: { style: "sng" } } },
  { text: " are behavior config files.", options: { color: "333333" } }
], {
  x: 5.55, y: 2.5, w: 4.2, h: 0.35,
  fontSize: 12, fontFace: "Microsoft YaHei"
});

// ===== Bottom note text (above footer) =====
slide.addText("Bottom supplementary description text, smaller font size, lighter color.", {
  x: 0.25, y: 4.67, w: 9.5, h: 0.32,
  fontSize: 9.5, color: "555555", fontFace: "Microsoft YaHei", valign: "middle"
});

// ===== Bottom footer =====
slide.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 5.0, w: 10, h: 0.625,
  fill: { color: "8B1A1A" }, line: { color: "8B1A1A" }
});
slide.addText("Left Organization Name", {
  x: 0.25, y: 5.0, w: 2.5, h: 0.625,
  fontSize: 13, bold: true, color: "FFFFFF",
  fontFace: "Microsoft YaHei", valign: "middle", margin: 0
});
slide.addText("Center contact or copyright info", {
  x: 2.5, y: 5.0, w: 5.5, h: 0.625,
  fontSize: 12, color: "FFFFFF", fontFace: "Microsoft YaHei",
  align: "center", valign: "middle", margin: 0
});
slide.addText("Page N", {
  x: 8.0, y: 5.0, w: 1.9, h: 0.625,
  fontSize: 13, bold: true, color: "FFFFFF",
  fontFace: "Microsoft YaHei", align: "right", valign: "middle", margin: 5
});

pres.writeFile({ fileName: "/mnt/user-data/outputs/output.pptx" });
console.log("Done!");
