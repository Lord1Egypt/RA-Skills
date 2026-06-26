import fs from "fs";
import path from "path";
import axios from "axios";
import sharp from "sharp";
import { createWorker } from "tesseract.js";
import { randomUUID } from "crypto";
const input = process.argv[2];
if (!input) {
    console.log("No image input");
    process.exit(1);
}
const baseDir = path.join(process.env.HOME || "~", "/openclaw-skill-data/");
const imageDir = path.join(baseDir, "image-knowledge-assets");
const dbFile = path.join(baseDir, "image-knowledge.json");
if (!fs.existsSync(imageDir)) {
    fs.mkdirSync(imageDir, { recursive: true });
}
if (!fs.existsSync(dbFile)) {
    fs.writeFileSync(dbFile, "[]");
}
async function saveImage(input) {
    const id = randomUUID();
    const filePath = path.join(imageDir, `${id}.png`);
    if (input.startsWith("http")) {
        const res = await axios.get(input, { responseType: "arraybuffer" });
        fs.writeFileSync(filePath, res.data);
    }
    else if (input.startsWith("data:image")) {
        const base64 = input.split(",")[1];
        const buffer = Buffer.from(base64, "base64");
        fs.writeFileSync(filePath, buffer);
    }
    else if (fs.existsSync(input)) {
        fs.copyFileSync(input, filePath);
    }
    else {
        throw new Error("Unknown image format");
    }
    return filePath;
}
async function preprocessImage(filePath) {
    const processed = filePath.replace(".png", "_processed.png");
    await sharp(filePath).grayscale().normalize().toFile(processed);
    return processed;
}
async function runOCR(imagePath) {
    const worker = await createWorker("chi_sim");
    const { data } = await worker.recognize(imagePath);
    await worker.terminate();
    return data.text;
}
function extractInfo(text) {
    const lines = text.split("\n").filter(v => v.trim());
    const summary = lines.slice(0, 3).join(" ");
    const keywords = lines
        .join(" ")
        .split(/[\s，。,:]/g)
        .filter(v => v.length > 1)
        .slice(0, 10);
    return { summary, keywords };
}
function saveKnowledge(record) {
    const db = JSON.parse(fs.readFileSync(dbFile, "utf-8"));
    db.push(record);
    fs.writeFileSync(dbFile, JSON.stringify(db, null, 2));
}
async function main() {
    console.log("Saving image...");
    const imagePath = await saveImage(input);
    console.log("Preprocessing image...");
    const processed = await preprocessImage(imagePath);
    console.log("Running OCR...");
    const text = await runOCR(processed);
    console.log("Extracting info...");
    const info = extractInfo(text);
    const record = {
        id: randomUUID(),
        time: new Date().toISOString(),
        image: imagePath,
        summary: info.summary,
        keywords: info.keywords,
        text: text
    };
    saveKnowledge(record);
    console.log("Saved knowledge:");
    console.log(JSON.stringify(record, null, 2));
}
main();
//# sourceMappingURL=index.js.map