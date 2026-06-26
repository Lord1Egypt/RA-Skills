import { getApiKey, httpsRequest, API_HOST, log, colors, success, error, info, safeJsonParse } from '../utils.js';

export async function createExam(options) {
  const apiKey = getApiKey(options.apiKey);

  const now = new Date();
  const todayStart = new Date(now.getFullYear(), now.getMonth(), now.getDate()).getTime();
  const weekFromNow = todayStart + 7 * 24 * 60 * 60 * 1000;

  const examDuration = options.duration ? parseInt(options.duration) : 60;

  const formConfig = {
    title: options.title || '未命名考试',
    content: options.desc || '',
    needExamMode: true,
    examDuration: examDuration,
    banViewExamResult: options.banViewResult === 'true',
    count: options.count ? parseInt(options.count) : 0,
    limitCount: false,
    allowBaomingCount: options.allowBaomingCount ? parseInt(options.allowBaomingCount) : 1,
    fixedNo: options.fixedNo !== 'false',
    noName: options.noName || '学号',
    nameLabel: options.nameLabel || '姓名',
    showNameList: true,
    dakaBtnText: options.btnText || '开始答卷',
    submitSuccessText: options.successText || '您已提交成功',
    isOpenRanking: options.ranking !== 'false',
    publishResult: options.publishResult === 'true',
    startTime: options.startTime ? new Date(options.startTime).getTime() : todayStart,
    endTime: options.endTime ? new Date(options.endTime).getTime() : weekFromNow,
    needTimeLimit: true
  };

  if (options.questions) {
    try {
      formConfig.examForms = safeJsonParse(options.questions, 'questions');
    } catch (err) {
      error(`考试题目解析失败: ${err.message}`);
      info('请确保 --questions 参数是有效的 JSON 数组格式');
      process.exit(1);
    }
  } else {
    formConfig.examForms = [
      {
        id: `${Date.now()}_1`,
        type: '1',
        title: '示例题目：以下哪项是正确的？',
        options: ['选项A', '选项B', '选项C', '选项D'],
        answer: '0',
        fullScore: 10,
        order: 1
      }
    ];
  }

  if (options.infoForms) {
    try {
      formConfig.infoForms = typeof options.infoForms === 'string'
        ? safeJsonParse(options.infoForms, 'info-forms')
        : options.infoForms;
    } catch (err) {
      error(`表单字段解析失败: ${err.message}`);
      info('请确保 --info-forms 参数是有效的 JSON 数组格式');
      process.exit(1);
    }
  }

  info('正在创建考试...');

  const mutation = `
    mutation CreateExam($input: TongjiInput!) {
      createTongjiByInput(input: $input) {
        _id
        title
        needExamMode
        examDuration
        examFullScore
        banViewExamResult
        isOpenRanking
        createdAt
        examForms {
          title
          type
          fullScore
          required
        }
      }
    }
`;

  const data = JSON.stringify({
    query: mutation,
    variables: { input: formConfig },
    operationName: 'createTongjiByInput'
  });

  try {
    const response = await httpsRequest(
      {
        hostname: API_HOST,
        port: 443,
        path: '/api/openapi/graphql',
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${apiKey}`,
          'Content-Length': Buffer.byteLength(data)
        }
      },
      data
    );

    if (response.data && response.data._id) {
      success('考试创建成功！');
      log(colors.bright, '   ID:', response.data._id);
      log(colors.bright, '   标题:', response.data.title);
      log(colors.bright, '   考试模式:', response.data.needExamMode ? '是' : '否');
      log(colors.bright, '   考试时长:', formConfig.examDuration, '分钟');
      if (response.data.examFullScore) log(colors.cyan, '   总分:', response.data.examFullScore);
      log(colors.cyan, '   题目数:', response.data.examForms?.length || 0);
      log(colors.cyan, '   禁止查看结果:', response.data.banViewExamResult ? '是' : '否');
      log(colors.cyan, '   显示排名:', response.data.isOpenRanking ? '是' : '否');
      log(colors.cyan, '   固定名单模式:', formConfig.fixedNo ? '是' : '否');

      if (formConfig.fixedNo && !options.nameList) {
        console.log('');
        log(colors.yellow, '⚠️  注意：当前使用固定名单模式，但未提供名单！');
        log(colors.yellow, '   只有名单中的人员才能参加考试。');
        log(
          colors.yellow,
          '   请在小程序管理后台导入考试名单，或使用 --no-fixed-no 关闭固定名单模式。'
        );
        console.log('');
      }

      if (options.qrcode) {
        info('正在生成二维码...');
        const { generateQrCode } = await import('./qrcode.js');
        await generateQrCode(response.data._id, { ...options, entityType: 'Tongji' });
      } else {
        info('使用以下命令生成二维码:');
        log(colors.cyan, `   miaoying qrcode ${response.data._id} --type exam`);
      }

      return response.data._id;
    } else {
      error('响应格式异常:', JSON.stringify(response));
      process.exit(1);
    }
  } catch (err) {
    error(err.message);
    process.exit(1);
  }
}
