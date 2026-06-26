#!/usr/bin/env node
/**
 * Google Calendar 일정 조회
 * 사용: node list.js [--date YYYY-MM-DD] [--days N] [--json]
 */

const { getCalendar } = require('./lib/gcal');
const { parseDate } = require('./lib/date-utils');
const yargs = require('yargs/yargs');
const { hideBin } = require('yargs/helpers');

const argv = yargs(hideBin(process.argv))
  .option('date', {
    type: 'string',
    description: '조회할 날짜 (today/tomorrow/YYYY-MM-DD)',
    default: 'today',
  })
  .option('days', {
    type: 'number',
    description: '조회할 일수',
    default: 1,
  })
  .option('json', {
    type: 'boolean',
    description: 'JSON 형식 출력',
    default: false,
  })
  .option('calendar', {
    type: 'string',
    description: '캘린더 ID (기본: primary)',
    default: process.env.GOOGLE_CALENDAR_ID || 'primary',
  })
  .help()
  .argv;

async function listEvents() {
  const calendar = await getCalendar();
  
  const startDate = parseDate(argv.date);
  const endDate = new Date(startDate);
  endDate.setDate(endDate.getDate() + argv.days);

  const res = await calendar.events.list({
    calendarId: argv.calendar,
    timeMin: startDate.toISOString(),
    timeMax: endDate.toISOString(),
    singleEvents: true,
    orderBy: 'startTime',
  });

  const events = res.data.items || [];

  if (argv.json) {
    console.log(JSON.stringify({ events }, null, 2));
    return;
  }

  // 텍스트 출력
  if (events.length === 0) {
    console.log('📅 일정 없음');
    return;
  }

  const grouped = {};
  events.forEach(event => {
    const start = event.start.dateTime || event.start.date;
    const dateKey = start.split('T')[0];
    if (!grouped[dateKey]) grouped[dateKey] = [];
    grouped[dateKey].push(event);
  });

  Object.keys(grouped).sort().forEach(dateKey => {
    const dayOfWeek = ['일', '월', '화', '수', '목', '금', '토'][new Date(dateKey).getDay()];
    console.log(`\n📅 ${dateKey} (${dayOfWeek})`);
    
    grouped[dateKey].forEach(event => {
      const start = event.start.dateTime || event.start.date;
      const end = event.end.dateTime || event.end.date;
      
      if (event.start.dateTime) {
        const startTime = new Date(start).toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit', hour12: false });
        const endTime = new Date(end).toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit', hour12: false });
        console.log(`  ${startTime}-${endTime}  ${event.summary}`);
      } else {
        console.log(`  종일  ${event.summary}`);
      }
      
      if (event.location) {
        console.log(`    📍 ${event.location}`);
      }
    });
  });
}

listEvents().catch(console.error);
