const http = require('http');
const { httpRequest, getBaseUrl } = require('../utils/http');
const { getOrStartServer } = require('../utils/server');

function listenForQuestion(sessionId, port, onResult) {
  const baseUrl = getBaseUrl('127.0.0.1', port);
  let lastCheck = Date.now();
  const timeoutMs = 120000;

  const checkQuestion = () => {
    http.get(`${baseUrl}/question`, (qRes) => {
      let qData = '';
      qRes.on('data', c => qData += c);
      qRes.on('end', () => {
        try {
          const questions = JSON.parse(qData);
          const sessionQuestion = questions?.find(q => q.sessionID === sessionId);
          if (sessionQuestion) {
            onResult({ 
              type: 'question', 
              question: sessionQuestion.questions[0].question,
              header: sessionQuestion.questions[0].header,
              options: sessionQuestion.questions[0].options,
              questionId: sessionQuestion.id
            });
          }
        } catch {}
      });
    }).on('error', () => {});

    if (Date.now() - lastCheck > timeoutMs) {
      onResult({ type: 'timeout' });
    }
  };

  const intervalId = setInterval(checkQuestion, 1000);
  checkQuestion();

  return () => clearInterval(intervalId);
}

function extractTextFromMessage(response) {
  if (!response || !response.parts) return '';
  
  const textParts = response.parts.filter(p => p.type === 'text');
  if (textParts.length > 0) {
    return textParts.map(p => p.text).join('\n');
  }
  
  if (response.info?.summary) {
    const summary = response.info.summary;
    if (summary.diffs?.length > 0) {
      return summary.diffs.map(d => `${d.file}: +${d.additions} -${d.deletions}`).join('\n');
    }
    if (summary.title) {
      return summary.title;
    }
  }
  
  return '';
}

async function continueSession(sessionId, userInput) {
  const { port, close } = await getOrStartServer();
  const baseUrl = getBaseUrl('127.0.0.1', port);

  const messageUrl = `${baseUrl}/session/${sessionId}/message`;
  const messageBody = JSON.stringify({
    parts: [{ type: 'text', text: userInput }],
    noReply: false
  });

  const questions = await httpRequest(`${baseUrl}/question`, { method: 'GET' });
  const pendingQuestion = questions?.find(q => q.sessionID === sessionId);
  
  if (pendingQuestion) {
    const replyUrl = `${baseUrl}/question/${pendingQuestion.id}/reply`;
    const replyBody = JSON.stringify({ answers: [[userInput]] });
    await httpRequest(replyUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: replyBody
    });
    console.log(`Answered question: ${pendingQuestion.questions[0].header}`);
  }

  console.log('Sending message, waiting for completion...');

  let messageResult = null;
  let messageError = null;
  let questionResult = null;
  let cleanup = null;

  const messageReq = http.request(messageUrl, {
    method: 'POST',
    headers: { 
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(messageBody)
    }
  }, (res) => {
    let data = '';
    res.on('data', chunk => data += chunk);
    res.on('end', () => {
      try {
        messageResult = JSON.parse(data);
      } catch {
        messageResult = data;
      }
    });
  });
  
  messageReq.on('error', (err) => {
    messageError = err.message;
  });

  messageReq.write(messageBody);
  messageReq.end();

  let checkDoneInterval = null;
  let questionCheckCleanup = null;

  await new Promise((resolve) => {
    checkDoneInterval = setInterval(() => {
      if (messageResult !== null || messageError) {
        clearInterval(checkDoneInterval);
        if (questionCheckCleanup) questionCheckCleanup();
        if (messageReq) messageReq.destroy();
        resolve();
      }
    }, 100);

    questionCheckCleanup = listenForQuestion(sessionId, port, (result) => {
      questionResult = result;
      clearInterval(checkDoneInterval);
      if (questionCheckCleanup) questionCheckCleanup();
      if (messageReq) messageReq.destroy();
      resolve();
    });
  });

  close();

  if (questionResult && questionResult.type === 'question') {
    return {
      success: true,
      type: 'question_pending',
      sessionId,
      question: questionResult.question,
      header: questionResult.header,
      options: questionResult.options.map(o => ({
        label: o.label,
        description: o.description
      })),
      questionId: questionResult.questionId
    };
  }

  if (messageError) {
    throw new Error(messageError);
  }

  const resultText = extractTextFromMessage(messageResult);
  
  return {
    success: true,
    type: 'completed',
    sessionId,
    result: resultText || 'Task completed'
  };
}

module.exports = {
  continueSession,
  listenForQuestion
};