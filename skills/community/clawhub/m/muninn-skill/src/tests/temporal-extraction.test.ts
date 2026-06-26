/**
 * Temporal Extraction Tests
 * 
 * Tests for the temporal extraction system that powers
 * LOCOMO benchmark temporal questions like:
 * "When did Caroline go to the LGBTQ support group?"
 */

import { extractDates, detectTemporalQuery, formatDate, formatDateRange } from '../extractors/temporal.js';

describe('Temporal Extraction', () => {
  describe('extractDates', () => {
    it('extracts absolute dates: "7 May 2023"', () => {
      const dates = extractDates('I went on May 7, 2023');
      expect(dates.length).toBeGreaterThan(0);
      const may7 = dates.find(d => d.originalText.includes('May') || d.originalText.includes('7'));
      expect(may7).toBeDefined();
      expect(may7?.dateType).toBe('absolute');
      expect(may7?.confidence).toBeGreaterThan(0.8);
    });

    it('extracts absolute dates: "2023-05-07" ISO format', () => {
      const dates = extractDates('The event was on 2023-05-07');
      expect(dates.length).toBeGreaterThan(0);
      const iso = dates.find(d => d.originalText.includes('2023-05-07'));
      expect(iso).toBeDefined();
      expect(iso?.dateType).toBe('absolute');
      expect(iso?.confidence).toBe(0.98);
    });

    it('extracts absolute dates: "7th March 2023" with ordinal', () => {
      const dates = extractDates('My birthday is 7th March 2023');
      expect(dates.length).toBeGreaterThan(0);
    });

    it('extracts month only: "August 2023"', () => {
      const dates = extractDates('In August 2023 I moved to Brisbane');
      expect(dates.length).toBeGreaterThan(0);
      const aug = dates.find(d => d.originalText.includes('August'));
      expect(aug).toBeDefined();
      expect(aug?.dateType).toBe('range'); // Month becomes a range
      expect(aug?.granularity).toBe('month');
    });

    it('extracts relative dates: "yesterday"', () => {
      const refDate = new Date('2023-05-10');
      const dates = extractDates('I went yesterday', refDate);
      expect(dates.length).toBeGreaterThan(0);
      const yesterday = dates.find(d => d.originalText === 'yesterday');
      expect(yesterday).toBeDefined();
      expect(yesterday?.dateType).toBe('relative');
      expect(yesterday?.date.toISOString().split('T')[0]).toBe('2023-05-09');
    });

    it('extracts relative dates: "tomorrow"', () => {
      const refDate = new Date('2023-05-10');
      const dates = extractDates('I will go tomorrow', refDate);
      expect(dates.length).toBeGreaterThan(0);
      const tomorrow = dates.find(d => d.originalText === 'tomorrow');
      expect(tomorrow).toBeDefined();
      expect(tomorrow?.date.toISOString().split('T')[0]).toBe('2023-05-11');
    });

    it('extracts relative dates: "last Tuesday"', () => {
      // May 10, 2023 is a Wednesday
      const refDate = new Date('2023-05-10'); 
      const dates = extractDates('I went last Tuesday', refDate);
      expect(dates.length).toBeGreaterThan(0);
      const lastTue = dates.find(d => d.originalText.includes('last Tuesday'));
      expect(lastTue).toBeDefined();
      // Last Tuesday from May 10 (Wednesday) would be May 9
      expect(lastTue?.date.toISOString().split('T')[0]).toBe('2023-05-09');
    });

    it('extracts relative dates: "next Monday"', () => {
      const refDate = new Date('2023-05-10'); // Wednesday
      const dates = extractDates('Meeting next Monday', refDate);
      expect(dates.length).toBeGreaterThan(0);
      const nextMon = dates.find(d => d.originalText.includes('next Monday'));
      expect(nextMon).toBeDefined();
      // Next Monday from May 10 would be May 15
      expect(nextMon?.date.toISOString().split('T')[0]).toBe('2023-05-15');
    });

    it('extracts relative dates: "3 weeks ago"', () => {
      const refDate = new Date('2023-05-15');
      const dates = extractDates('I went 3 weeks ago', refDate);
      expect(dates.length).toBeGreaterThan(0);
      const weeksAgo = dates.find(d => d.originalText.includes('3 weeks ago'));
      expect(weeksAgo).toBeDefined();
      // 3 weeks before May 15 is April 24
      expect(weeksAgo?.date.toISOString().split('T')[0]).toBe('2023-04-24');
    });

    it('extracts relative dates: "in 2 days"', () => {
      const refDate = new Date('2023-05-10');
      const dates = extractDates('Starting in 2 days', refDate);
      expect(dates.length).toBeGreaterThan(0);
      const in2Days = dates.find(d => d.originalText.includes('in 2 days'));
      expect(in2Days).toBeDefined();
      expect(in2Days?.date.toISOString().split('T')[0]).toBe('2023-05-12');
    });

    it('extracts date ranges: "this week"', () => {
      // May 10, 2023 is a Wednesday
      const refDate = new Date('2023-05-10');
      const dates = extractDates('This week has been busy', refDate);
      expect(dates.length).toBeGreaterThan(0);
      const thisWeek = dates.find(d => d.originalText.includes('this week'));
      expect(thisWeek).toBeDefined();
      expect(thisWeek?.dateType).toBe('range');
      // This week should start on Monday (May 8) and end Sunday (May 14)
      expect(thisWeek?.date.toISOString().split('T')[0]).toBe('2023-05-08');
    });

    it('extracts date ranges: "last month"', () => {
      const refDate = new Date('2023-05-15');
      const dates = extractDates('Last month was great', refDate);
      expect(dates.length).toBeGreaterThan(0);
      const lastMonth = dates.find(d => d.originalText.includes('last month'));
      expect(lastMonth).toBeDefined();
      expect(lastMonth?.dateType).toBe('range');
      expect(lastMonth?.date.toISOString().split('T')[0]).toBe('2023-04-01');
    });

    it('extracts date ranges: "the week before 6 July 2023"', () => {
      const dates = extractDates('the week before 6 July 2023');
      expect(dates.length).toBeGreaterThan(0);
      const weekBefore = dates.find(d => d.originalText.includes('week before'));
      expect(weekBefore).toBeDefined();
      expect(weekBefore?.dateType).toBe('range');
      // Week before July 6 should be June 29 - July 5
      expect(weekBefore?.date.toISOString().split('T')[0]).toBe('2023-06-29');
    });

    it('extracts multiple dates from a single text', () => {
      const text = 'On May 7, 2023 I went to the doctor, and then on June 15, 2023 I had a follow-up. Last year I moved to Brisbane.';
      const dates = extractDates(text);
      expect(dates.length).toBeGreaterThanOrEqual(2);
    });

    it('returns empty array for text without dates', () => {
      const dates = extractDates('This is just a regular sentence with no temporal information');
      expect(dates.length).toBe(0);
    });
  });

  describe('detectTemporalQuery', () => {
    it('detects "When did..." questions', () => {
      const result = detectTemporalQuery('When did Caroline go to the LGBTQ support group?');
      expect(result.isTemporal).toBe(true);
      expect(result.temporalType).toBe('when');
    });

    it('detects "When was..." questions', () => {
      const result = detectTemporalQuery('When was the project launched?');
      expect(result.isTemporal).toBe(true);
      expect(result.temporalType).toBe('when');
    });

    it('detects "What day..." questions', () => {
      const result = detectTemporalQuery('What day is the meeting?');
      expect(result.isTemporal).toBe(true);
      expect(result.temporalType).toBe('what_day');
    });

    it('detects "What time..." questions', () => {
      const result = detectTemporalQuery('What time does the train leave?');
      expect(result.isTemporal).toBe(true);
      expect(result.temporalType).toBe('what_time');
    });

    it('detects "How long..." questions', () => {
      const result = detectTemporalQuery('How long did it take?');
      expect(result.isTemporal).toBe(true);
      expect(result.temporalType).toBe('duration');
    });

    it('detects "How often..." questions', () => {
      const result = detectTemporalQuery('How often do you go to the gym?');
      expect(result.isTemporal).toBe(true);
      expect(result.temporalType).toBe('frequency');
    });

    it('returns false for non-temporal questions', () => {
      const result = detectTemporalQuery('What is the capital of France?');
      expect(result.isTemporal).toBe(false);
      expect(result.temporalType).toBeNull();
    });

    it('extracts dates from the query itself', () => {
      const result = detectTemporalQuery('When did you go on May 7, 2023?');
      expect(result.isTemporal).toBe(true);
      expect(result.extractedDates.length).toBeGreaterThan(0);
    });
  });

  describe('formatDate', () => {
    it('formats date in ISO format', () => {
      const date = new Date('2023-05-07');
      const formatted = formatDate(date, 'iso');
      expect(formatted).toBe('2023-05-07');
    });

    it('formats date in readable format', () => {
      const date = new Date('2023-05-07');
      const formatted = formatDate(date, 'readable');
      expect(formatted).toBe('May 07, 2023');
    });
  });

  describe('formatDateRange', () => {
    it('formats a date range', () => {
      const start = new Date('2023-06-29');
      const end = new Date('2023-07-05');
      const formatted = formatDateRange(start, end, 'iso');
      expect(formatted).toBe('2023-06-29/2023-07-05');
    });
  });
});
