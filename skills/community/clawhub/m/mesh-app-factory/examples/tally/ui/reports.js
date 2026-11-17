const HOUR_MS=3600000;

export default {
inject:['service', 'tags'],
data() {return {
    range:{from:'',to:'',iFrom:0,iTo:0},
    proxyRange:{from:'',to:''},//不能直接用range，否则会null异常，不知原因
    mainCharts:null,
    byOpts:[],
    type:'day', //day,hour
    list:[]    
}},
created(){
    var dt=new Date();
    this.range.to=date2str(dt);
    var cur=parseInt(dt.getTime()/HOUR_MS);
    dt.setTime((cur-6*24)*HOUR_MS);
    this.range.from=date2str(dt);
    this.byOpts=[{label:this.tags.report.byDay,value:'day'},
        {label:this.tags.report.byHour,value:'hour'}]
},
mounted(){
    //必须Vue.markRaw，否则首次会出错，提示‘Cannot read properties of undefined (reading ‘type‘)’
    this.mainCharts=Vue.markRaw(echarts.init(document.getElementById('mainCharts')));
    this.query();
},
methods:{
query() {
    var dt=new Date(this.range.to);
    dt.setHours(0,0,0);
    this.range.iTo=parseInt(dt.getTime()/HOUR_MS)+24;
    dt=new Date(this.range.from);
    dt.setHours(0,0,0);
    this.range.iFrom=parseInt(dt.getTime()/HOUR_MS);
    var url="/api/report/stats?from="+this.range.iFrom+"&to="+this.range.iTo;
    request({method:"GET",url:url}, this.service.name).then(resp=>{
        var list=resp.code==RetCode.OK?resp.data.data:[];
        this.list=list;
        this.stat();
    })
},
statByDay(from, to) {
    var data={};
    var one={};
    var list=[];
    var xDt;
    var ll=this.list;
    var dt=new Date();
    var hour=from;
    var foreHour=from;

    //at,vip,nOrder,vOrder,nService,vService,brokerage
    for(var l of ll) {
        hour=l[0];
        if(hour-foreHour>24) {
            for(var h=foreHour==from?from:(foreHour+24);h<hour;h+=24) {
                dt.setTime(h*HOUR_MS);//按小时汇总
                xDt=(dt.getMonth()+1)+'.'+dt.getDate();
                one={at:xDt,vip:0,nOrder:0,nService:0,vOrder:0,vService:0,brokerage:0}
                data[xDt]=one;
                list.push(one);
            }
        }
        dt.setTime(hour*HOUR_MS);//按小时汇总
        xDt=(dt.getMonth()+1)+'.'+dt.getDate();
        one=data[xDt];
        if(!one) {
            one={at:xDt,vip:0,nOrder:0,nService:0,vOrder:0,vService:0,brokerage:0}
            data[xDt]=one;
            list.push(one);
        }
        one.vip+=l[1];
        one.nOrder+=l[2];
        one.vOrder+=l[3];
        one.nService+=l[4];
        one.vService+=l[5];
        one.brokerage+=l[6];
        foreHour=hour;
    }
    var h;
    if(foreHour==from) {
        h=from;
    } else {
        dt.setTime((24+foreHour)*HOUR_MS);
        dt.setHours(0,0,0);
        h=parseInt(dt.getTime()/HOUR_MS);
    }
    for(;h<to;h+=24) {
        dt.setTime(h*HOUR_MS);
        xDt=(dt.getMonth()+1)+'.'+dt.getDate();
        list.push({at:xDt,vip:0,nOrder:0,nService:0,vOrder:0,vService:0,brokerage:0});
    }
    return list;
},
statByHour() {
    var one={};
    var list=[];
    var ll=this.list;
    var dt=new Date();
    var hour;

    for(var i=0;i<24;i++) {
        list.push({at:(i>9?i:'0'+i),vip:0,nOrder:0,nService:0,vOrder:0,vService:0,brokerage:0})
    }
    //at,vip,nOrder,vOrder,nService,vService,brokerage
    for(var l of ll) {
        dt.setTime(l[0]*3600000);//按小时汇总
        hour=dt.getHours();
        one=list[hour];
        one.vip+=l[1];
        one.nOrder+=l[2];
        one.vOrder+=l[3];
        one.nService+=l[4];
        one.vService+=l[5];
        one.brokerage+=l[6];
    }
    return list;
},
stat() {
    var x=[];
    var vip=[];
    var nOrder=[];
    var nService=[];
    var vOrder=[];
    var vService=[];
    var brokerage=[];

    var data;
    if(this.type=='day') {
        data=this.statByDay(this.range.iFrom, this.range.iTo);
    } else {
        data=this.statByHour();
    }
    for(var d of data) {
        x.push(d.at);
        vip.push(d.vip);
        nOrder.push(d.nOrder);
        nService.push(d.nService);
        vOrder.push(d.vOrder);
        vService.push(d.vService);
        brokerage.push(d.brokerage);
    }
    var rt=this.tags.report;
    var series=[
        {name:rt.vip,type:'line',data:vip,yAxisIndex:0,itemStyle:{color:"#ff0011"}}, //新增会员数
        {name:rt.nOrder,type:'line',data:nOrder,yAxisIndex:0,itemStyle:{color:"#11ff00"}}, //新增订单数
        {name:rt.nService,type:'line',data:nService,yAxisIndex:0,itemStyle:{color:"#115500"}}, //新增服务数
        {name:rt.vOrder,type:'bar',data:vOrder,yAxisIndex:1,itemStyle:{color:"#0000ff"}}, //新增订单金额
        {name:rt.vService,type:'bar',data:vService,yAxisIndex:1,itemStyle:{color:"#5555ff"}}, //新增服务金额
        {name:rt.vBrokerage,type:'bar',data:brokerage,yAxisIndex:1,itemStyle:{color:"#9999ff"}} //新增提成
    ];

    this.mainCharts.setOption({
        title:{show:false},
        tooltip:{},
        legend:{},
        xAxis:{data:x},
        yAxis:[{name:this.tags.unit.T},{name:this.tags.unit.Y}],
        series:series
    });
},
dateChanged() {
    if(this.proxyRange) {
        copyObjTo(this.proxyRange, this.range);
        this.query();
    }
},
rangeFilter(dt) {
    var now=new Date().getTime();
    var t=Date.parse(dt);
    return t<=now&&t>=now-90*24*HOUR_MS;
}
},

template:`
<q-layout view="hHh lpr fFf">
<q-header class="bg-grey-1 text-primary">
 <q-toolbar>
  <q-btn flat round icon="arrow_back" dense @click="service.back"></q-btn>
  <q-toolbar-title>{{tags.report.title}}</q-toolbar-title>
  <q-space></q-space>
  <q-btn flat round dense icon="menu"><q-menu>
   <q-option-group :options="byOpts" type="radio" v-model="type"
    @update:model-value="stat()" style="min-width:10em"></q-option-group>
  </q-menu></q-btn>
 </q-toolbar>
</q-header>
<q-page-container>
 <q-page class="q-pa-md">
  <div id="mainCharts" :style="{width:'95vw', height:'80vh'}"></div>
  <div class="text-center">
  <q-btn icon="event" flat dense>
   <q-popup-proxy cover transition-show="scale" transition-hide="scale">
    <q-date v-model="proxyRange" range :options="rangeFilter">
     <div class="row items-center justify-end">
      <q-btn :label="tags.ok" color="primary" @click="dateChanged" v-close-popup></q-btn>
      <q-btn :label="tags.close" color="primary" flat v-close-popup></q-btn>
     </div>
    </q-date>
   </q-popup-proxy>
   {{range.from}} => {{range.to}}
  </q-btn>
  </div>
 </q-page>
</q-page-container>
</q-layout>
`
}