export default {
inject:['service', 'tags'],
data() {return {
    beginTime:0,
    days:7,
    pkgId:0,
    mainCharts:null,
    pkgCharts:null,
    revenueCharts:null,
    date:'',
    dateStr:'',
    packageOpts:[],
    mainList:[],
    pkgList:[],
    dlgs:{main:false,pkg:false}
}},
created(){
    var end=new Date();
    this.beginTime=end.getTime()-7*86400000;
    var start=new Date(this.beginTime);
    this.dateStr=start.getFullYear()+'-'+(start.getMonth()+1)+'-'+start.getDate()
     +"  "+end.getFullYear()+'-'+(end.getMonth()+1)+'-'+end.getDate();
},
mounted(){
    //必须Vue.markRaw，否则首次会出错，提示‘Cannot read properties of undefined (reading ‘type‘)’
    this.mainCharts=Vue.markRaw(echarts.init(document.getElementById('mainCharts')));
    this.pkgCharts=Vue.markRaw(echarts.init(document.getElementById('pkgCharts')));
    this.revenueCharts=Vue.markRaw(echarts.init(document.getElementById('revenueCharts')));
    this.query_main();
    this.service.getPackages().then(data =>{
        this.packageOpts=data.opts;
        this.pkgId=data.pkgs[0].id;
        this.query_pkg();
        this.query_revenue();
    }).catch(err=>{
        Console.info(err);
    });
},
methods:{
query_main() {
    var beginTime=Math.ceil(this.beginTime/7200000);
    var url="/api/report/main?beginTime="+beginTime+"&days="+this.days;
    request({method:"GET",url:url}, this.service.name).then(resp=>{
        var list=resp.code==RetCode.OK?resp.data.data:[];
        //reportAt,vipNum,revenue,orderNum,logNum
        var vipNum=[];
        var revenue=[];
        var orderNum=[];
        var reportAt=[];
        var dt=new Date();
        var foreDay='', dayNo;
        var xDt;
        var mainList=[];

        for(var l of list) {
            dt.setTime(l[0]*7200000);//按2小时为时长汇总
            dayNo=(dt.getMonth()+1)+'.'+dt.getDate();
            
            if(foreDay==dayNo) {
                xDt=dt.getHours()+':00';
            } else {
                xDt=dayNo+'/'+dt.getHours()+':00';
                foreDay=dayNo;
            }
            reportAt.push(xDt);
            vipNum.push(l[1]);
            revenue.push(l[2]);
            orderNum.push(l[3]);
            mainList.push([dt.toLocaleString(), l[1], l[2], l[3], l[4]])
        }
        this.mainList = mainList;
        var series=[
            {name:this.tags.revenue,type:'line',data:revenue,yAxisIndex:0,itemStyle:{color:"#ff0011"}}, //新增收入
            {name:this.tags.vipNum,type:'bar',data:vipNum,yAxisIndex:1,itemStyle:{color:"#11ff00"}}, //新增会员(个)
            {name:this.tags.orderNum,type:'bar',data:orderNum,yAxisIndex:1,itemStyle:{color:"#0011ff"}} //新增订单
        ];
        
        this.mainCharts.setOption({
            title: {show:false},
            tooltip: {},
            legend:{},
            xAxis: {data:reportAt},
            yAxis: [{name:this.tags.unit.Y},{name:this.tags.unit.T}],
            series: series
        });
    })
},
query_pkg() {
    var beginTime=Math.ceil(this.beginTime/86400000);
    var url="/api/report/package?beginTime="+beginTime+"&days="+this.days+"&pkgId="+this.pkgId;
    request({method:"GET",url:url}, this.service.name).then(resp=>{
        var list=resp.code==RetCode.OK?resp.data.data:[];
        //reportAt,revenue,orderNum,orderBal,logNum,logVal
        var revenue=[];
        var orderBal=[];
        var logVal=[];
        var reportAt=[];
        var dt=new Date();
        var xDt;
        var pkgList=[];
        
        for(var l of list) {
            dt.setTime(l[0]*86400000);
            xDt = (dt.getMonth()+1)+'.'+dt.getDate();
            reportAt.push(xDt);
            revenue.push(l[1]);
            orderBal.push(l[3]);
            logVal.push(l[5]);
            pkgList.push([xDt, l[1], l[2], l[3], l[4], l[5]]);
        }
        this.pkgList = pkgList;
        var series=[
            {name:this.tags.revenue,type:'line',data:revenue,yAxisIndex:0,itemStyle:{color:"#ff0011"}}, //新增收入(元)
            {name:this.tags.orderBal,type:'bar',data:orderBal,yAxisIndex:1,stack:'balance',itemStyle:{color:"#11ff00"}},//剩余服务
            {name:this.tags.logVal,type:'bar',data:logVal,yAxisIndex:1,stack:'balance',itemStyle:{color:"#0011ff"}}//当天服务
        ];
        
        this.pkgCharts.setOption({
            title: {show:false},
            tooltip: {},
            legend:{},
            xAxis: {data:reportAt},
            yAxis: [{name:this.tags.unit.Y},{name:this.tags.unit.T}],
            series: series
        });
    })
},
pkg_changed() {
    this.query_pkg();
},
query_revenue() {
    var pkgs='';
    for(var p of this.packageOpts) {
        if(pkgs!='') {
            pkgs += ',';
        }
        pkgs += p.value;
    }
    
    var beginTime=Math.ceil(this.beginTime/86400000);
    var url="/api/report/revenue?beginTime="+beginTime+"&days="+this.days+"&pkgs="+pkgs;
    request({method:"GET",url:url}, this.service.name).then(resp => {
        var list=resp.code==RetCode.OK?resp.data.data:[];
        var pkgList={};
        for(var p of this.packageOpts) {
            pkgList[p.value]=[];
        }
        //pkgId,reportAt,revenue
        var reportAt=[];
        var dt=new Date();
        var xDt, oldDt = '';
        var n = 0;
        
        for(var l of list) {
            dt.setTime(l[1]*86400000);
            xDt = (dt.getMonth()+1)+'.'+dt.getDate();
            if(xDt != oldDt) { //按日期排序后返回
                n = reportAt.length;
                for(var i in pkgList) {
                    if(pkgList[i].length<n) {
                        pkgList[i].push(0); //不是每个套餐每天都有数据，所以补齐缺少的数据
                    }
                }
                oldDt=xDt;
                reportAt.push(xDt);
            }
            pkgList[l[0]].push(l[2]);
        }

        var series=[];
        for(var p of this.packageOpts) {
            series.push({
                name:p.label,
                type:'line',
                data:pkgList[p.value],
                yAxisIndex:0
            });
        }
        
        this.revenueCharts.setOption({
            title: {show:false},
            tooltip: {},
            legend:{},
            xAxis: {data:reportAt},
            yAxis: [{name:this.tags.unit.Y}],
            series: series
        });
    })
},
date_range_end(range) {
    var f=range.from;
    var t=range.to;
    this.dateStr=f.year+'/'+f.month+'/'+f.day + "  " + t.year+'/'+t.month+'/'+t.day;
    
    var ft=new Date(f.year,f.month-1,f.day);
    var tt=new Date(t.year,t.month-1,t.day);
    this.beginTime=ft.getTime();
    this.days = Math.ceil((tt.getTime()-this.beginTime)/86400000);
    if(this.days <= 31) {
        this.query_pkg();
        this.query_main();
        this.query_revenue();
    } else {
        this.$refs.errMsg.show(this.tags.exceedsDayNum);
    }
}
},

template:`
<q-layout view="hHh lpr fFf">
  <q-header class="bg-grey-1 text-primary" elevated>
   <q-toolbar>
      <q-btn flat round icon="arrow_back" dense @click="service.go_back"></q-btn>
      <q-toolbar-title>{{tags.reports}}</q-toolbar-title>
   </q-toolbar>
  </q-header>
  <q-page-container>
    <q-page class="q-pa-md">
    
<q-input filled v-model="dateStr">
  <template v-slot:prepend>
    <q-icon name="event" class="cursor-pointer">
      <q-popup-proxy transition-show="scale" transition-hide="scale">
        <q-date v-model="date" range @range-end="date_range_end">
          <div class="row items-center justify-end">
            <q-btn v-close-popup :label="tags.close" color="primary" flat></q-btn>
          </div>
        </q-date>
      </q-popup-proxy>
    </q-icon>
  </template>
</q-input>
<div class="text-h6">{{tags.mainReports}}<q-icon name="list" @click="dlgs.main=true" color="primary" class="q-ml-lg"></q-icon></div>
<div id="mainCharts" :style="{width:'100vw', height:'40vh'}"></div>
<q-space></q-space>
<q-select v-model="pkgId" emit-value map-options :options="packageOpts" @update:model-value="pkg_changed"></q-select>
<div class="text-h6">{{tags.pkgReports}}<q-icon name="list" @click="dlgs.pkg=true" color="primary" class="q-ml-lg"></q-icon></div>
<div id="pkgCharts" :style="{width:'100vw', height:'40vh'}"></div>
<div class="text-h6">{{tags.revenueReports}}</div>
<div id="revenueCharts" :style="{width:'100vw', height:'40vh'}"></div>
    </q-page>
  </q-page-container>
</q-layout>

<q-dialog v-model="dlgs.main">
 <q-card>
  <q-card-section class="row items-center q-pb-none">
   <div class="text-h6">{{tags.mainReports}}</div>
   <q-space></q-space>
   <q-btn icon="close" flat round dense v-close-popup></q-btn>
  </q-card-section>
  <q-card-section class="q-pt-none">
   <q-markup-table flat><tbody>
     <thead><tr>
      <th class="text-left">{{tags.reportAt}}</th>
      <th class="text-right">{{tags.vipNum}}</th>
      <th class="text-right">{{tags.revenue}}</th>
      <th class="text-right">{{tags.orderNum}}</th>
      <th class="text-right">{{tags.logNum}}</th>
     </tr></thead>
     <tbody><tr v-for="l in mainList" clickable>
      <td class="text-left">{{l[0]}}</td>
      <td class="text-right">{{l[1]}}</td>
      <td class="text-right">{{l[2]}}</td>
      <td class="text-right">{{l[3]}}</td>
      <td class="text-right">{{l[4]}}</td>
     </tr></tbody>
  </q-markup-table>
 </q-card>
</q-dialog>

<q-dialog v-model="dlgs.pkg">
 <q-card>
  <q-card-section class="row items-center q-pb-none">
   <div class="text-h6">{{tags.pkgReports}}</div>
   <q-space></q-space>
   <q-btn icon="close" flat round dense v-close-popup></q-btn>
  </q-card-section>
  <q-card-section class="q-pt-none">
   <q-markup-table flat><tbody>
     <thead><tr>
      <th class="text-left">{{tags.reportAt}}</th>
      <th class="text-right">{{tags.revenue}}</th>
      <th class="text-right">{{tags.orderNum}}</th>
      <th class="text-right">{{tags.orderBal}}</th>
      <th class="text-right">{{tags.logNum}}</th>
      <th class="text-right">{{tags.logVal}}</th>
     </tr></thead>
     <tbody><tr v-for="l in pkgList" clickable>
      <td class="text-left">{{l[0]}}</td>
      <td class="text-right">{{l[1]}}</td>
      <td class="text-right">{{l[2]}}</td>
      <td class="text-right">{{l[3]}}</td>
      <td class="text-right">{{l[4]}}</td>
      <td class="text-right">{{l[5]}}</td>
     </tr></tbody>
  </q-markup-table>
 </q-card>
</q-dialog>

<component-alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" ref="errMsg"></component-alert-dialog>
`
}