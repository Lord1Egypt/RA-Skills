---
name: mini-program-dev
description: 微信小程序开发辅助。提供代码模板、API 示例、常见问题解答。
metadata:
  {
    "openclaw": {
      "requires": {},
      "install": []
    }
  }
---

# 微信小程序开发辅助

## 常用代码模板

### 页面结构

```javascript
// pages/demo/demo.js
Page({
  data: {
    message: 'Hello',
    list: [],
    loading: false
  },

  onLoad(options) {
    // 页面加载
    this.fetchData();
  },

  onShow() {
    // 页面显示
  },

  onPullDownRefresh() {
    // 下拉刷新
    this.fetchData().then(() => {
      wx.stopPullDownRefresh();
    });
  },

  fetchData() {
    this.setData({ loading: true });
    return new Promise((resolve, reject) => {
      wx.request({
        url: 'https://api.example.com/data',
        success: res => {
          this.setData({ 
            list: res.data,
            loading: false 
          });
          resolve(res);
        },
        fail: reject
      });
    });
  },

  handleTap(e) {
    console.log('tap', e.currentTarget.dataset);
  }
})
```

```xml
<!-- pages/demo/demo.wxml -->
<view class="container">
  <text class="title">{{message}}</text>
  
  <block wx:for="{{list}}" wx:key="id">
    <view class="item" bindtap="handleTap" data-id="{{item.id}}">
      {{item.name}}
    </view>
  </block>

  <loading wx:if="{{loading}}">加载中...</loading>
</view>
```

```css
/* pages/demo/demo.wxss */
.container {
  padding: 20rpx;
}

.title {
  font-size: 32rpx;
  font-weight: bold;
  display: block;
  margin-bottom: 20rpx;
}

.item {
  padding: 20rpx;
  border-bottom: 1rpx solid #eee;
}
```

### 常用 API

```javascript
// 提示框
wx.showToast({ title: '成功', icon: 'success' });
wx.showModal({ title: '提示', content: '确认？' });

// 跳转页面
wx.navigateTo({ url: '/pages/detail/detail?id=1' });
wx.redirectTo({ url: '/pages/detail/detail' });
wx.switchTab({ url: '/pages/index/index' });

// 存储
wx.setStorageSync('key', 'value');
const value = wx.getStorageSync('key');

// 授权
wx.getUserProfile({
  success: res => {
    console.log(res.userInfo);
  }
});

// 支付
wx.requestPayment({
  timeStamp: '',
  nonceStr: '',
  package: '',
  signType: 'MD5',
  paySign: '',
  success: () => {},
  fail: () => {}
});
```

### 组件通信

```javascript
// 父组件 → 子组件
// parent.wxml
<child-component id="child" data="{{parentData}}" />

// parent.js
this.selectComponent('#child').childMethod();

// 子组件 → 父组件
// child.js
this.triggerEvent('myEvent', { detail: 'data' });

// child.wxml
<view bind:myEvent="handleEvent" />

// parent.wxml
<child-component bind:myEvent="handleEvent" />
```

### TabBar 配置

```json
// app.json
{
  "pages": [
    "pages/index/index",
    "pages/profile/profile"
  ],
  "window": {
    "navigationBarTitleText": "我的小程序"
  },
  "tabBar": {
    "color": "#999",
    "selectedColor": "#1890ff",
    "list": [
      {
        "pagePath": "pages/index/index",
        "text": "首页",
        "iconPath": "/icons/home.png",
        "selectedIconPath": "/icons/home-active.png"
      },
      {
        "pagePath": "pages/profile/profile",
        "text": "我的",
        "iconPath": "/icons/user.png",
        "selectedIconPath": "/icons/user-active.png"
      }
    ]
  }
}
```

---

## 常见问题

### 1. 页面不刷新
检查是否在 `onShow` 而非 `onLoad` 中处理数据刷新。

### 2. 授权失败
记得在 `app.json` 的 `permission` 中声明权限：
```json
{
  "permission": {
    "scope.userLocation": {
      "desc": "用于展示附近内容"
    }
  }
}
```

### 3. 安卓真机调试
使用 vConsole 查看日志：
```javascript
wx.vibrateLong(); // 震动提示
```

---

需要具体页面的代码吗？告诉我你的需求 📱
