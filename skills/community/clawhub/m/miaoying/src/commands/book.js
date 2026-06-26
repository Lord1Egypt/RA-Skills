import { getApiKey, httpsRequest, API_HOST, log, colors, success, error, info, safeJsonParse } from '../utils.js';

export async function createBooking(options) {
  const apiKey = getApiKey(options.apiKey);

  const now = new Date();
  const todayStart = new Date(now.getFullYear(), now.getMonth(), now.getDate()).getTime();
  const weekFromNow = todayStart + 7 * 24 * 60 * 60 * 1000;

  let allowSubmitTimeRules = [];
  let dayRepeatCount = 1;

  if (options.slots) {
    dayRepeatCount = parseInt(options.slots);
    if (dayRepeatCount === 1) {
      allowSubmitTimeRules = [
        {
          _id: 1,
          startTime: '07:00',
          endTime: '23:59',
          notifyTime: '07:00'
        }
      ];
    } else if (dayRepeatCount === 2) {
      allowSubmitTimeRules = [
        {
          _id: 1,
          startTime: '07:00',
          endTime: '09:00',
          notifyTime: '07:00'
        },
        {
          _id: 2,
          startTime: '12:00',
          endTime: '14:00',
          notifyTime: '12:00'
        }
      ];
    } else if (dayRepeatCount === 3) {
      allowSubmitTimeRules = [
        {
          _id: 1,
          startTime: '07:00',
          endTime: '09:00',
          notifyTime: '07:00'
        },
        {
          _id: 2,
          startTime: '12:00',
          endTime: '14:00',
          notifyTime: '12:00'
        },
        {
          _id: 3,
          startTime: '18:00',
          endTime: '20:00',
          notifyTime: '18:00'
        }
      ];
    }
  }

  const formConfig = {
    title: options.title || '未命名预约',
    content: options.desc || '',
    needBookMode: true,
    dayRepeatCount: dayRepeatCount,
    allowSubmitTimeRules: allowSubmitTimeRules,
    repeatDays: [0, 1, 2, 3, 4, 5, 6],
    repeatStartDate: todayStart,
    repeatEndDate: weekFromNow,
    count: options.count ? parseInt(options.count) : 20,
    limitCount: options.limitCount !== 'false',
    allowBaomingCount: options.allowBaomingCount ? parseInt(options.allowBaomingCount) : 1,
    fixedNo: options.fixedNo === 'true' || options.fixedNo === true,
    noName: options.noName || '序号',
    allowBuka: options.allowBuka !== 'false',
    needNotify: options.needNotify === 'true',
    notifyTime: options.notifyTime
      ? parseInt(options.notifyTime.split(':')[0]) * 3600000 +
        parseInt(options.notifyTime.split(':')[1]) * 60000
      : 32400000,
    publishResult: options.publishResult !== 'false'
  };

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
  } else {
    formConfig.infoForms = [
      { title: '姓名', required: true, type: '0' },
      { title: '手机号', required: true, type: '11' }
    ];
    formConfig.requiredFields = ['姓名', '手机号'];
  }

  if (options.startTime) formConfig.startTime = new Date(options.startTime).getTime();
  if (options.endTime) formConfig.endTime = new Date(options.endTime).getTime();

  if (options.userLimit) formConfig.allowBaomingCount = parseInt(options.userLimit);

  info('正在创建预约...');

  const mutation = `
    mutation CreateBooking($input: TongjiInput!) {
      createTongjiByInput(input: $input) {
        _id
        title
        needBookMode
        dayRepeatCount
        allowSubmitTimeRules {
          startTime
          endTime
        }
        repeatDays
        createdAt
        infoForms {
          title
          type
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
      success('预约创建成功！');
      log(colors.bright, '   ID:', response.data._id);
      log(colors.bright, '   标题:', response.data.title);
      log(colors.bright, '   预约模式:', response.data.needBookMode ? '是' : '否');
      log(colors.bright, '   每天时段数:', response.data.dayRepeatCount);
      if (response.data.allowSubmitTimeRules && response.data.allowSubmitTimeRules.length > 0) {
        log(colors.cyan, '   预约时段:');
        response.data.allowSubmitTimeRules.forEach((rule, index) => {
          log(colors.cyan, `     ${index + 1}. ${rule.startTime} - ${rule.endTime}`);
        });
      }
      log(
        colors.cyan,
        '   表单字段:',
        response.data.infoForms?.map(f => f.title).join(', ') || '无'
      );
      log(colors.cyan, '   固定名单模式:', formConfig.fixedNo ? '是' : '否');

      if (formConfig.fixedNo && !options.nameList) {
        console.log('');
        log(colors.yellow, '⚠️  注意：当前使用固定名单模式，但未提供名单！');
        log(colors.yellow, '   只有名单中的人员才能预约。');
        log(
          colors.yellow,
          '   请在小程序管理后台导入预约名单，或移除 --fixed-no 参数关闭固定名单模式。'
        );
        console.log('');
      }

      if (options.qrcode) {
        info('正在生成二维码...');
        const { generateQrCode } = await import('./qrcode.js');
        await generateQrCode(response.data._id, { ...options, entityType: 'Booking' });
      } else {
        info('使用以下命令生成二维码:');
        log(colors.cyan, `   miaoying qrcode ${response.data._id} --type booking`);
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
