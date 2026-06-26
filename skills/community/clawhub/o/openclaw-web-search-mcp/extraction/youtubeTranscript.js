const { execSync } = require("child_process");
const fs = require("fs");
const path = require("path");

/**
 * Parse SRT subtitle format to JSON
 * @param {string} srtContent - The SRT content as string
 * @returns {Array} Array of subtitle entries
 */
function parseSRT(srtContent) {
  const lines = srtContent.split('\n');
  const entries = [];
  let currentEntry = null;

  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed) continue;

    // Check if line is a number (entry index)
    if (/^\d+$/.test(trimmed)) {
      if (currentEntry) {
        entries.push(currentEntry);
      }
      currentEntry = { text: '' };
    } else if (currentEntry && trimmed.includes('-->')) {
      // Time line: 00:00:00,000 --> 00:00:05,000
      const [start, end] = trimmed.split(' --> ');
      currentEntry.start = timeToSeconds(start);
      currentEntry.duration = timeToSeconds(end) - currentEntry.start;
    } else if (currentEntry) {
      // Text line
      currentEntry.text += (currentEntry.text ? ' ' : '') + trimmed;
    }
  }

  if (currentEntry) {
    entries.push(currentEntry);
  }

  return entries;
}

/**
 * Convert time string to seconds
 * @param {string} timeStr - Time in format 00:00:00,000
 * @returns {number} Time in seconds
 */
function timeToSeconds(timeStr) {
  const [time, ms] = timeStr.split(',');
  const [hours, minutes, seconds] = time.split(':').map(Number);
  return hours * 3600 + minutes * 60 + seconds + Number(ms) / 1000;
}

/**
 * Fetch YouTube transcript using yt-dlp
 * @param {string} url - YouTube video URL
 * @returns {Promise<{transcript: string, segments: Array}>}
 */
async function getTranscript(url) {
  try {
    // Temporary filename for subtitles
    const tmpFile = path.join(__dirname, "tmp_subtitles.en.srt");

    // Run yt-dlp to extract auto-generated subtitles in SRT format
    // --skip-download avoids downloading video
    // --write-auto-sub gets auto captions
    // --sub-lang en only English
    // --convert-subs srt converts to SRT
    execSync(`/home/nishu/.local/bin/yt-dlp "${url}" --skip-download --write-auto-sub --sub-lang en --convert-subs srt --output "tmp_subtitles"`, { stdio: "ignore", cwd: __dirname });

    // Read subtitles SRT
    if (!fs.existsSync(tmpFile)) {
      return { transcript: "", segments: [], error: "No subtitles found" };
    }

    const raw = fs.readFileSync(tmpFile, "utf-8");
    fs.unlinkSync(tmpFile); // cleanup

    const subs = parseSRT(raw);

    if (!subs || subs.length === 0) {
      return { transcript: "", segments: [], error: "No subtitles entries" };
    }

    // Build full transcript and segments
    const segments = subs.map(e => ({
      text: e.text,
      start: e.start,
      duration: e.duration
    }));

    const transcript = segments.map(s => s.text).join(" ");

    return { transcript, segments };

  } catch (error) {
    return { transcript: "", segments: [], error: error.message };
  }
}

module.exports = { getTranscript };