Page({
  data: {
    products: [
      { id: 1, name: '手工陶杯 · 月白', price: '128', sold: 234, tag: '新', tone: '#fde6c8' },
      { id: 2, name: '宋代茶则 · 黑檀', price: '168', sold: 89, tag: '限', tone: '#dde7d4' },
      { id: 3, name: '《设计的觉醒》原研哉', price: '88', sold: 512, tag: '荐', tone: '#e8dcd0' },
      { id: 4, name: '黄铜书签套装 · 三枚', price: '58', sold: 321, tag: '', tone: '#f4dccd' },
      { id: 5, name: '柴烧建盏 · 兔毫', price: '288', sold: 41, tag: '限', tone: '#d8d4c5' },
      { id: 6, name: '日记本 · 夏布封面', price: '78', sold: 168, tag: '', tone: '#e9e1d0' }
    ]
  },
  onCardTap(e) {
    const id = e.currentTarget.dataset.id;
    console.log('tap product', id);
  }
});
