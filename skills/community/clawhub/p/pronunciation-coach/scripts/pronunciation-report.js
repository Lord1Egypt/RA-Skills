#!/usr/bin/env node
// Pronunciation Assessment Report Generator
// Pipe Azure Speech JSON into this script for a human-readable report.
// Usage: echo '<json>' | node pronunciation-report.js

let input = '';
process.stdin.on('data', chunk => input += chunk);
process.stdin.on('end', () => {
  try {
    const data = JSON.parse(input);

    if (data.RecognitionStatus !== 'Success') {
      console.log(`❌ Recognition failed: ${data.RecognitionStatus}`);
      return;
    }

    const best = data.NBest[0];

    console.log('🐰 PRONUNCIATION ASSESSMENT REPORT');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('');
    console.log('📊 OVERALL SCORES:');
    console.log(`  🎯 Pronunciation: ${best.PronScore}/100`);
    console.log(`  ✅ Accuracy:      ${best.AccuracyScore}/100`);
    console.log(`  💨 Fluency:       ${best.FluencyScore}/100`);
    console.log(`  🎵 Prosody:       ${best.ProsodyScore}/100`);
    console.log(`  📝 Completeness:  ${best.CompletenessScore}/100`);
    console.log('');
    console.log(`  Recognized: "${best.Display}"`);
    console.log('');

    console.log('📖 WORD-BY-WORD BREAKDOWN:');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');

    const problemWords = [];
    const problemPhonemes = [];

    for (const word of best.Words) {
      const score = word.AccuracyScore;
      const emoji = score >= 90 ? '✅' : score >= 70 ? '⚠️' : '❌';
      console.log(`  ${emoji} "${word.Word}" — ${score}/100`);

      if (word.ErrorType && word.ErrorType !== 'None') {
        console.log(`     Error: ${word.ErrorType}`);
      }

      if (score < 95 && word.Phonemes) {
        for (const ph of word.Phonemes) {
          if (ph.AccuracyScore < 90) {
            const phEmoji = ph.AccuracyScore >= 70 ? '⚠️' : '❌';
            console.log(`     ${phEmoji} Phoneme /${ph.Phoneme}/ — ${ph.AccuracyScore}/100`);
            problemPhonemes.push({ word: word.Word, phoneme: ph.Phoneme, score: ph.AccuracyScore });
          }
        }
      }

      if (score < 85) {
        problemWords.push({ word: word.Word, score });
      }
    }

    console.log('');

    if (problemPhonemes.length > 0) {
      console.log('🔍 SOUNDS THAT NEED WORK:');
      console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
      for (const p of problemPhonemes) {
        console.log(`  ⚠️ /${p.phoneme}/ in "${p.word}" — scored ${p.score}/100`);
      }
      console.log('');
    }

    if (problemWords.length > 0) {
      console.log('📌 WORDS TO PRACTICE:');
      console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
      for (const w of problemWords) {
        console.log(`  🎯 "${w.word}" — ${w.score}/100`);
      }
      console.log('');
    }

    const prosodyIssues = [];
    for (const word of best.Words) {
      if (word.Feedback?.Prosody?.Break?.ErrorTypes) {
        for (const err of word.Feedback.Prosody.Break.ErrorTypes) {
          if (err !== 'None') {
            prosodyIssues.push({ word: word.Word, issue: err });
          }
        }
      }
      if (word.Feedback?.Prosody?.Intonation?.ErrorTypes) {
        for (const err of word.Feedback.Prosody.Intonation.ErrorTypes) {
          prosodyIssues.push({ word: word.Word, issue: `Intonation: ${err}` });
        }
      }
    }

    if (prosodyIssues.length > 0) {
      console.log('🎵 PROSODY/INTONATION ISSUES:');
      console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
      for (const p of prosodyIssues) {
        console.log(`  ⚠️ "${p.word}" — ${p.issue}`);
      }
      console.log('');
    }

    const overall = best.PronScore;
    let verdict;
    if (overall >= 95) verdict = '🌟 Excellent! Near-native pronunciation.';
    else if (overall >= 85) verdict = '👍 Very good! Minor refinements needed.';
    else if (overall >= 70) verdict = '📈 Good effort! Some sounds need practice.';
    else if (overall >= 50) verdict = '💪 Keep going! Several areas to improve.';
    else verdict = '🏋️ Needs work. Focus on the problem sounds above.';

    console.log('🏆 VERDICT: ' + verdict);

  } catch (e) {
    console.error('Error parsing results:', e.message);
    console.log('Raw input:', input.substring(0, 500));
  }
});
