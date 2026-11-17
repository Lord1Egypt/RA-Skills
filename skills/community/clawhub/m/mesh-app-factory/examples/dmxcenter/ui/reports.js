const WEEKDAY_HOURS=7*24;
const HOUR_MS=3600000;
export default {
inject:['service', 'tags'],
data() {return {
    charts:null,
    begin:0, //小时单位，7天内看小时，否则看天
    end:0,//小时单位，默认一个月
    date:'',
    dateStr:'',
}},
created(){
    var dt=new Date();
    this.end=Math.ceil(dt.getTime()/HOUR_MS);
    var begin=this.end - WEEKDAY_HOURS;
    var dt1=new Date(begin*HOUR_MS)
    var dt2=new Date(dt1.getFullYear(), dt1.getMonth(),dt1.getDate(),0,0,0,0);
    this.begin=Math.ceil(dt2.getTime()/HOUR_MS);
    this.dateStr=dt2.toLocaleDateString()+' - '+dt.toLocaleDateString();
    this.queryReports();
},
mounted(){ //mounted在created之后
    this.charts=Vue.markRaw(echarts.init(document.getElementById('charts')));
},
methods:{
queryReports() {
    var url="/api/report/report?begin="+this.begin+"&end="+this.end;
    request({method:"GET",url:url},this.service.name).then(resp=>{
        if(resp.code!=RetCode.OK) {
            this.$refs.errDlg.showErr(resp.code, resp.info);
            return;
        }
        //reportAt,sendMsg,sentMsg,addDevice,sellDevice
        var send=[], sent=[], add=[], sell=[];
        var iAt=resp.data.cols.indexOf('reportAt');
        var iSend=resp.data.cols.indexOf('sendMsg');
        var iSent=resp.data.cols.indexOf('sentMsg');
        var iAdd=resp.data.cols.indexOf('addDevice');
        var iSell=resp.data.cols.indexOf('sellDevice');

        var xAxis=[];
        var dt=new Date(this.begin*HOUR_MS);
        var hours=this.end - this.begin;
        var tUnit=1; //1小时一个统计单位
        if(hours >WEEKDAY_HOURS*10) {
            tUnit=WEEKDAY_HOURS; //7天一个统计单位
        } else if(hours>WEEKDAY_HOURS) {
            tUnit=24; //1天一个统计单位
        }
        
        var fore,cur;
        var end=this.end*HOUR_MS;
        if(hours>WEEKDAY_HOURS) {//按天显示
            var ms=tUnit*HOUR_MS;
            for(var t=dt.getTime();t<end;t+=ms) {
                dt.setTime(t);
                cur=dt.getFullYear()+'/'+(dt.getMonth()+1);
                if(fore==cur) {
                    xAxis.push(dt.getDate());
                }else{
                    fore=cur;
                    xAxis.push(cur+'/'+dt.getDate());
                }
            }
        } else { //按小时显示
            for(var t=dt.getTime();t<end;t+=HOUR_MS) {
                dt.setTime(t);
                cur=(dt.getMonth()+1)+'/'+dt.getDate();
                if(fore==cur) {
                    xAxis.push(dt.getHours()+':00');
                } else {
                    fore=cur;
                    xAxis.push(dt.getHours()+':00('+cur+')');
                }
            }
        }
        for(var i in xAxis) {
            send.push(0);
            sent.push(0);
            add.push(0);
            sell.push(0);
        }
        var l,reportAt, n;
        for(var i in resp.data.data) {
            l=resp.data.data[i];
            reportAt=l[iAt];
            n = Math.floor((reportAt-this.begin)/tUnit);
            send[n]+=l[iSend];
            sent[n]+=l[iSent];
            add[n]+=l[iAdd];
            sell[n]+=l[iSell];
        }
        this.charts.setOption({
            title: {show:false},
            tooltip: {},
            grid: {left:'0%',containLabel:true},
            legend: {type:'scroll',bottom:10},
            xAxis: {data:xAxis},
            yAxis: [{name:this.tags.reports.msgUnit,minInterval:1},{name:this.tags.reports.devUnit}],
            series: [
                {name:this.tags.reports.sendMsg,type:'bar',data:send,yAxisIndex:0},
                {name:this.tags.reports.sentMsg,type:'bar',data:sent,yAxisIndex:0},
                {name:this.tags.reports.addDevice,type:'line',data:add,yAxisIndex:1},
                {name:this.tags.reports.sellDevice,type:'line',data:sell,yAxisIndex:1}
            ]
        });
    })
},
date_range_end(range) {
    var f=range.from;
    var t=range.to;
    var ft=new Date(f.year,f.month-1,f.day);
    var tt=new Date(t.year,t.month-1,t.day);
    this.dateStr=ft.toLocaleDateString()+' - '+tt.toLocaleDateString();
    this.begin=Math.ceil(ft.getTime()/HOUR_MS);
    this.end=Math.ceil(tt.getTime()/HOUR_MS)+24; //包括最后一整天
    var days=Math.ceil((this.end-this.begin)/24);
    if(days<=366) {
        this.queryReports();
    } else {
        this.$refs.errMsg.show(this.tags.exceedsDayNum);
    }
}
},

template:`
<q-layout view="hHh lpr fFf">
<q-header>
 <q-toolbar>
  <q-btn flat round icon="arrow_back" dense @click="service.go_back"></q-btn>
  <q-toolbar-title>{{tags.reports.name}}</q-toolbar-title>
 </q-toolbar>
</q-header>
<q-footer class="bg-white text-primary q-pa-md">
 <q-input v-model="dateStr">
  <template v-slot:prepend>
   <q-icon name="event" class="cursor-pointer">
    <q-popup-proxy transition-show="scale" transition-hide="scale">
     <q-date v-model="date" range @range-end="date_range_end" minimal>
      <div class="row items-center justify-end">
       <q-btn v-close-popup :label="tags.close" color="primary" flat></q-btn>
      </div>
     </q-date>
    </q-popup-proxy>
   </q-icon>
  </template>
 </q-input>
</q-footer>

<q-page-container>
  <q-page class="q-pa-md">
   <div id="charts" :style="{width:'100vw', height:'70vh'}"></div>
  </q-page>
</q-page-container>
</q-layout>
<component-alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" :close="tags.close" ref="errDlg"></component-alert-dialog>
`
}