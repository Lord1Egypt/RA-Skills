Page({
  data: {
    isRecording: false,
    voiceText: '',
    redPacket: null,
    recentRecords: []
  },

  onLoad() {
    this.loadRecentRecords();
  },

  // 开始语音识别
  async startVoiceRecord() {
    const that = this;
    
    if (this.data.isRecording) {
      this.stopVoiceRecord();
      return;
    }

    this.setData({ isRecording: true });

    // 使用微信同声传译插件进行语音识别
    const recorderManager = wx.getRecorderManager();
    
    recorderManager.onStart(() => {
      console.log('录音开始');
    });

    recorderManager.onStop((res) => {
      console.log('录音停止', res);
      // 调用语音识别 API
      that.recognizeVoice(res.tempFilePath);
    });

    // 录音 10 秒后自动停止
    setTimeout(() => {
      recorderManager.stop();
    }, 10000);

    recorderManager.start({
      duration: 10000,
      sampleRate: 16000,
      numberOfChannels: 1,
      encodeBitRate: 48000
    });
  },

  stopVoiceRecord() {
    const recorderManager = wx.getRecorderManager();
    recorderManager.stop();
    this.setData({ isRecording: false });
  },

  // 语音识别（模拟模式 - 测试号用）
  async recognizeVoice(filePath) {
    const that = this;
    
    wx.showLoading({ title: '识别中...' });

    // 模拟语音识别结果（测试号用）
    setTimeout(() => {
      wx.hideLoading();
      
      // 模拟识别结果（确保没有隐藏字符）
      const mockText = '你好你好给我。老婆，李婉瑜发一个红包，祝他节日快乐！';
      
      console.log('模拟识别结果:', mockText);
      console.log('文本长度:', mockText.length);
      console.log('文本字符码:', Array.from(mockText).map(c => c.charCodeAt(0)));
      
      that.setData({ voiceText: mockText });
      
      // 解析语音指令
      that.parseVoiceCommand(mockText);
      
      wx.showToast({ 
        title: '模拟识别成功', 
        icon: 'success',
        duration: 2000
      });
    }, 1000);
  },

  // 解析语音指令
  parseVoiceCommand(text) {
    const that = this;  // 保存 this 引用
    
    console.log('开始解析语音指令:', text);
    console.log('文本长度:', text.length);
    
    // 去除所有空格和标点符号，方便匹配
    const cleanText = text.replace(/[\s,.!?.,]/g, '');
    console.log('清理后文本:', cleanText);
    
    // 简单测试：检查是否包含关键词
    const hasRedPacket = cleanText.includes('红包');
    const hasLaopo = cleanText.includes('老婆');
    const hasLiWanyu = cleanText.includes('李婉瑜');
    
    console.log('关键词检查:', { hasRedPacket, hasLaopo, hasLiWanyu });
    
    if (hasRedPacket && (hasLaopo || hasLiWanyu)) {
      console.log('✅ 匹配到红包指令');
      
      // 提取金额（数字）
      const amountMatch = cleanText.match(/(\d+)/);
      const amount = amountMatch ? parseInt(amountMatch[1]) : 520;  // 默认 520
      
      // 提取收款人
      let recipient = '老婆';
      if (hasLiWanyu) {
        recipient = '李婉瑜';
      }
      
      // 提取祝福语（最后一个逗号或句号后的内容）
      const lastCommaIndex = text.lastIndexOf(',');
      const lastPeriodIndex = text.lastIndexOf('.');
      const separatorIndex = Math.max(lastCommaIndex, lastPeriodIndex);
      const message = separatorIndex > 0 ? text.substring(separatorIndex + 1).trim() : '恭喜发财，大吉大利';
      
      console.log('解析成功:', { recipient, amount, message });
      
      // 强制设置数据并刷新页面
      that.setData({
        redPacket: {
          recipient: recipient,
          amount: amount,
          message: message
        }
      }, function() {
        console.log('setData 回调执行，redPacket:', that.data.redPacket);
        wx.showToast({ title: '解析成功', icon: 'success' });
      });
      
      that.setData({ isRecording: false });
      return;
    }
    
    // 如果没有匹配到
    wx.showToast({ title: '没听明白，再说一次', icon: 'none' });
    console.log('未匹配到红包指令');
    that.setData({ isRecording: false });
  },

  // 发送红包（模拟模式 - 测试号用）
  sendRedPacket() {
    const that = this;
    const { redPacket } = this.data;

    wx.showLoading({ title: '发送中...' });

    // 模拟发送成功（测试号用）
    setTimeout(() => {
      wx.hideLoading();
      
      console.log('模拟发送成功:', redPacket);
      
      // 生成红包卡片
      that.generateRedPacketCard(redPacket);
      
      wx.showToast({ title: '发送成功', icon: 'success' });
      
      // 清空预览
      that.setData({ redPacket: null, voiceText: '' });
      
      // 添加模拟记录
      const mockRecord = {
        _id: 'mock_' + Date.now(),
        recipient: redPacket.recipient,
        amount: redPacket.amount,
        message: redPacket.message,
        createTime: new Date().toISOString()
      };
      
      that.setData({ 
        recentRecords: [mockRecord, ...that.data.recentRecords]
      });
    }, 500);
  },

  // 生成红包卡片
  generateRedPacketCard(redPacket) {
    // 生成红包分享卡片（可以分享到微信）
    const cardData = {
      title: `¥${redPacket.amount} 红包`,
      desc: redPacket.message,
      path: `/pages/record/record?id=${Date.now()}`
    };

    // 提示用户分享
    wx.showModal({
      title: '红包已生成',
      content: `给 ${redPacket.recipient} 的 ${redPacket.amount} 元红包已生成！\n\n"${redPacket.message}"\n\n点击右上角分享给对方`,
      confirmText: '去分享',
      success: function(res) {
        if (res.confirm) {
          // 可以调用微信分享 API
          console.log('用户去分享');
        }
      }
    });
  },

  // 加载最近记录（模拟模式 - 测试号用）
  loadRecentRecords() {
    const that = this;
    
    // 模拟加载记录（测试号用）
    const mockRecords = [
      {
        _id: 'mock_1',
        recipient: '老婆',
        amount: 520,
        message: '我爱你~',
        createTime: new Date().toISOString()
      },
      {
        _id: 'mock_2',
        recipient: '老妈',
        amount: 200,
        message: '母亲节快乐',
        createTime: new Date(Date.now() - 86400000).toISOString()
      }
    ];
    
    that.setData({ recentRecords: mockRecords });
    console.log('模拟加载记录:', mockRecords);
  }
})
