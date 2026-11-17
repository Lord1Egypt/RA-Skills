export default {
inject:['tags','service'],
data(){return{
  stats:{},
  topProducts:[],
  trendsData:[],
  startDate:'',
  endDate:'',
  dateRange:'',
  profit:{},
  profitRate:'0.0'
}},

created(){
  this.initDateRange();
  this.loadStats();
  this.loadTopProducts();
  this.loadSalesTrend();
  this.loadProfit();
},

methods:{
  initDateRange(){
    var now=new Date();
    var year=now.getFullYear();
    var month=now.getMonth()+1;
    var day=now.getDate();
    this.startDate=year+'-'+(month<10?'0'+month:month)+'-01';
    this.endDate=year+'-'+(month<10?'0'+month:month)+'-'+(day<10?'0'+day:day);
    this.dateRange=this.startDate+' - '+this.endDate;
  },

  loadStats(){
    var start=new Date(this.startDate).getTime();
    var end=new Date(this.endDate).getTime();
    request({method:"GET",url:"/api/report/stats?startDate="+start+"&endDate="+end},this.service.name).then(resp=>{
      if(resp.code!=RetCode.OK) {
        this.stats=[];
        return;
      }
      this.stats=resp.data;
    });
  },

  loadTopProducts(){
    var start=new Date(this.startDate).getTime();
    var end=new Date(this.endDate).getTime();
    request({method:"GET",url:"/api/report/topProducts?limit=10&startDate="+start+"&endDate="+end},this.service.name).then(resp=>{
      if(resp.code!=RetCode.OK){
        this.topProducts=[];
        return;
      }
      this.topProducts=resp.data.list||[];
    });
  },

  loadSalesTrend(){
    var start=new Date(this.startDate).getTime();
    var end=new Date(this.endDate).getTime();
    request({method:"GET",url:"/api/report/salesTrend?startDate="+start+"&endDate="+end},this.service.name).then(resp=>{
      if(resp.code!=RetCode.OK) {
        this.trendsData=[];
      } else {
        this.trendsData=resp.data.data||[];
      }
      this.renderChart();
    });
  },

  loadProfit(){
    var start=new Date(this.startDate).getTime();
    var end=new Date(this.endDate).getTime();
    request({method:"GET",url:"/api/report/profit?startDate="+start+"&endDate="+end},this.service.name).then(resp=>{
      if(resp.code!=RetCode.OK) {
        this.profit={};
        return;
      }
      this.profit=resp.data;
      var s=this.profit.saleAmount||0;
      this.profitRate=s>0?((this.profit.profit||0)/s*100).toFixed(1):'0.0';
    });
  },

  renderChart(){
    if(!this.$refs.chartRef) return;
    var chart=echarts.init(this.$refs.chartRef);
    var dt=new Date();
    var dates=[];
    var sales=[];
    var purchases=[];
    var lastDt, dts;
    for(var t of this.trendsData) {
        if(t.type=='SAL') {
            sales.push(t.amount);
        } else {
            purchases.push(t.amount);
        }
        dt.setTime(t.day*86400000);
        dts=date2str(dt);
        if(dts != lastDt) {
            lastDt=dts;
            dates.push(dts);
        }
    }
    chart.setOption({
      tooltip:{trigger:'axis'},
      xAxis:{type:'category',data:dates},
      yAxis:{type:'value',name:this.tags.amount},
      series:[
        {name:this.tags.salesAmount,type:'line',data:sales,smooth:true,areaStyle:{opacity:0.3}},
        {name:this.tags.purchaseAmount,type:'line',data:purchases,smooth:true,areaStyle:{opacity:0.1}}
      ]
    });
  },

  onDateRangeEnd(range){
    if(!range.from||!range.to) return;
    var fromYear=range.from.year;
    var fromMonth=range.from.month;
    var fromDay=range.from.day||1;
    var toYear=range.to.year;
    var toMonth=range.to.month;
    var toDay=range.to.day||new Date(toYear,toMonth,0).getDate();

    this.startDate=fromYear+'-'+(fromMonth<10?'0'+fromMonth:fromMonth)+'-'+(fromDay<10?'0'+fromDay:fromDay);
    this.endDate=toYear+'-'+(toMonth<10?'0'+toMonth:toMonth)+'-'+(toDay<10?'0'+toDay:toDay);
    this.dateRange=this.startDate+' - '+this.endDate;

    this.loadStats();
    this.loadTopProducts();
    this.loadSalesTrend();
    this.loadProfit();
  }
},

template:`
<q-layout view="lHh lpr lFf" container style="height:100vh">
<q-header elevated class="bg-primary text-white">
  <q-toolbar>
    <q-btn flat icon="arrow_back" @click="$router.push('/home')"></q-btn>
    <q-toolbar-title>{{tags.stats}}</q-toolbar-title>
  </q-toolbar>
</q-header>

<q-page-container>
<q-page padding>
  <!-- 日期选择器 -->
  <q-card class="q-mb-md">
    <q-card-section class="row items-center">
      <q-icon name="event" class="q-mr-sm"></q-icon>
      <div class="text-subtitle1">{{tags.dateRange}}</div>
      <q-space></q-space>
      <q-input v-model="dateRange" readonly dense style="width:250px">
        <template v-slot:prepend>
          <q-icon name="event" class="cursor-pointer">
            <q-popup-proxy transition-show="scale" transition-hide="scale">
              <q-date v-model="startDate" range @range-end="onDateRangeEnd" minimal>
                <div class="row items-center justify-end q-pa-sm">
                  <q-btn v-close-popup :label="tags.close" color="primary" flat></q-btn>
                </div>
              </q-date>
            </q-popup-proxy>
          </q-icon>
        </template>
      </q-input>
    </q-card-section>
  </q-card>

  <div class="text-h5 q-mb-md">{{tags.stats}}</div>

  <!-- 毛利统计 -->
  <div class="row q-col-gutter-md q-mb-lg">
    <div class="col-12 col-sm-6 col-md-3">
      <q-card class="bg-positive text-white">
        <q-card-section>
          <div class="text-h6">{{tags.saleAmount}}</div>
          <div class="text-h4">¥{{profit.saleAmount||0}}</div>
        </q-card-section>
      </q-card>
    </div>
    <div class="col-12 col-sm-6 col-md-3">
      <q-card class="bg-primary text-white">
        <q-card-section>
          <div class="text-h6">{{tags.profit}}</div>
          <div class="text-h4">¥{{profit.profit||0}}</div>
        </q-card-section>
      </q-card>
    </div>
    <div class="col-12 col-sm-6 col-md-3">
      <q-card>
        <q-card-section>
          <div class="text-h6">{{tags.purchaseAmount}}</div>
          <div class="text-h4">¥{{profit.purchaseAmount||0}}</div>
        </q-card-section>
      </q-card>
    </div>
    <div class="col-12 col-sm-6 col-md-3">
      <q-card>
        <q-card-section>
          <div class="text-h6">{{tags.profitRate}}</div>
          <div class="text-h4">{{profitRate}}%</div>
        </q-card-section>
      </q-card>
    </div>
  </div>

  <!-- 统计数据卡片 -->
  <div class="row q-col-gutter-md q-mb-lg">
    <div class="col-12 col-sm-6 col-md-3">
      <q-card>
        <q-card-section>
          <div class="text-h6 text-primary">{{stats.productCount||0}}</div>
          <div class="text-subtitle2">{{tags.productCount}}</div>
        </q-card-section>
      </q-card>
    </div>
    <div class="col-12 col-sm-6 col-md-3">
      <q-card>
        <q-card-section>
          <div class="text-h6 text-positive">¥{{stats.todaySales||0}}</div>
          <div class="text-subtitle2">{{tags.todaySales}}</div>
        </q-card-section>
      </q-card>
    </div>
    <div class="col-12 col-sm-6 col-md-3">
      <q-card>
        <q-card-section>
          <div class="text-h6 text-positive">¥{{stats.monthSales||0}}</div>
          <div class="text-subtitle2">{{tags.monthSales}}</div>
        </q-card-section>
      </q-card>
    </div>
    <div class="col-12 col-sm-6 col-md-3">
      <q-card>
        <q-card-section>
          <div class="text-h6 text-negative">{{stats.lowStockCount||0}}</div>
          <div class="text-subtitle2">{{tags.lowStockAlert}}</div>
        </q-card-section>
      </q-card>
    </div>
  </div>

  <!-- 图表区域 -->
  <div class="row q-col-gutter-md">
    <div class="col-12 col-md-6">
      <q-card>
        <q-card-section><div class="text-h6 q-mb-md">{{tags.salesTrend}}</div></q-card-section>
        <q-card-section><div ref="chartRef" style="height:300px;"></div></q-card-section>
      </q-card>
    </div>
    <div class="col-12 col-md-6">
      <q-card>
        <q-card-section><div class="text-h6 q-mb-md">{{tags.topProducts}}</div></q-card-section>
        <q-list bordered separator>
          <q-item v-for="(item,index) in topProducts" :key="index">
            <q-item-section>
              <q-item-label>{{item.name}}</q-item-label>
              <q-item-label caption>{{item.category}} - {{tags.quantity}}: {{item.totalQty}}</q-item-label>
            </q-item-section>
            <q-item-section side>
              <div class="text-weight-bold text-positive">¥{{item.totalAmount}}</div>
            </q-item-section>
          </q-item>
          <q-item v-if="!topProducts.length">
            <q-item-section><q-item-label class="text-grey">{{tags.noData}}</q-item-label></q-item-section>
          </q-item>
        </q-list>
      </q-card>
    </div>
  </div>
</q-page>
</q-page-container>
</q-layout>
`
}
