const SERVICE="bios";
const DAY_MS=86400000;
const HOUR_MS=3600000;

export default {
inject:['service', 'tags'],
data() {return {
    name:this.$route.query.service,
    key:"",
    caller:{list:[], name:[], features:""},
    config:{list:[], name:"", val:""},
    nodes:[],
    dbList:[],
    dbNo:0,
    pubSrvs:[],
    vipSrvs:[],
    stats:{dlg:false,chart:null,width:0,date:{from:'',to:''},proxyDate:{from:'',to:''},errMsg:''}
}},
created() {
    var dt=new Date();
    var to=dt.getFullYear()+'/'+(dt.getMonth()+1)+'/'+dt.getDate();
    dt.setTime(dt.getTime()-3*DAY_MS);
    var from=dt.getFullYear()+'/'+(dt.getMonth()+1)+'/'+dt.getDate();
    this.stats.date={from:from,to:to};
    this.stats.width=document.documentElement.clientWidth*0.7;
    this.query_service();
    this.query_servers();
},
methods:{
query_service() {
    var url="/service/detail?service=" + this.name;
    this.service.request_private({method:"GET",url:url}, SERVICE).then(resp => {
        if(!resp || resp.code != RetCode.OK) {
            if(resp.code == RetCode.NOT_EXISTS) {
                this.clear_service();
                return;
            }
            this.$refs.errDlg.showErr(resp.code, resp.info);
            return;
        }
        this.key=resp.data.key;
        this.caller.list=resp.data.callers;
        this.dbNo=resp.data.dbNo;
        this.handleConfigs(resp);
        this.pwds=resp.data.pwds;
        var dbList=[];
        
        resp.data.dbs.forEach(db=>{ //name(dbname.type),val(type),ut
            var pos = db.name.lastIndexOf('.');
            var name=db.name.substr(0, pos);

            var type='storage';
            if(db.val=="tdb") {
                type="device_hub";
            } else if(db.val=="sdb") {
                type="search";
            }

            dbList.push({name:name,type:type,sType:db.val});
        });
        this.dbList=dbList;
    })
},
query_servers() {
    var url="/status/serviceNodes?service=" + this.name;
    this.service.request_private({method:"GET",url:url}, SERVICE).then(resp => {
        if(!resp || resp.code != RetCode.OK || !resp.data) {
            return;
        }
        this.nodes=resp.data.nodes.map(n=>{
            var v=n.ver;
            n.ver=Math.floor(v/1000000)+'.'+(Math.floor(v/1000)%1000)+'.'+(v%1000);
            return n;
        });//service,partId,addr,status,ver
    })
},
set_key(){
    var opts={method:"PUT",url:"/service/setKey",
        data:{service:this.name, key:this.key}};
    this.service.request_private(opts,SERVICE).then(resp=>{
        if(!resp || resp.code != RetCode.OK) {
            this.$refs.errDlg.showErr(resp.code, resp.info);
        } else {
            this.$refs.dlg_set_key.hide();
        }
    });
},
set_dbNo(){
    var opts={method:"PUT",url:"/service/setDbNo",
        data:{service:this.name, no:this.dbNo}};
    this.service.request_private(opts, SERVICE).then(resp=>{
        if(!resp || resp.code != RetCode.OK) {
            this.$refs.errDlg.showErr(resp.code, resp.info);
        } else {
            this.$refs.dlg_set_dbNo.hide();
        }
    });
},
caller_resp(resp) {
    if(!resp || resp.code != RetCode.OK) {
        this.$refs.errDlg.showErr(resp.code, resp.info);
        return;
    }
    this.caller.list=resp.data.callers;
    this.caller.name=[];
    this.caller.features="";
    this.$refs.dlg_add_caller.hide();
},
add_caller(){
    var opts={method:"POST", url:"/service/addCaller",
        data:{service:this.name,caller:this.caller.name[0],
         features:this.caller.features}};
    this.service.request_private(opts,SERVICE).then(this.caller_resp);   
},
remove_caller(caller){
    var opts={method:"DELETE",
     url:"/service/removeCaller?service="+this.name+"&caller="+caller};
    this.service.request_private(opts,SERVICE).then(this.caller_resp);
},
handleConfigs(resp) {
    var cfgs = {};
    var configs=resp.data.configs;
    for(let i in configs) {
        var k=configs[i].name;
        var v=configs[i].val;
        if(v.length < 45) {
            cfgs[k]=v;
        } else {
            cfgs[k]=v.substr(0,20)+"..."+v.substr(v.length-20);
        }
    }
    this.config.list=cfgs;
},
config_resp(resp) {
    if(!resp || resp.code != 0) {
        this.$refs.errDlg.showErr(resp.code, resp.info);
        return;
    }
    this.config.name="";
    this.config.val="";
    this.service.request_private({method:"GET",url:"/service/getConfigs?service="+this.name}, SERVICE).then(this.handleConfigs);
},
add_config(){
    var opts={method:"PUT", url:"/service/setConfig",
        data:{service:this.name,name:this.config.name,val:this.config.val}};
    this.service.request_private(opts, SERVICE).then(resp => {
        this.config_resp(resp);
        this.$refs.dlg_add_config.hide();   
    });
},
remove_config(itemName){
    var opts={method:"DELETE",
     url:"/service/removeConfig?service="+this.name+"&name="+itemName};
    this.service.request_private(opts,SERVICE).then(this.config_resp);
},
refeshSrvs(resp) {
    if(resp.code != RetCode.OK) {
        this.$refs.errDlg.showErr(resp.code, resp.info);
        return;
    }
    this.query_servers();
},
initDbs() {//调用服务的initdb接口，初始化数据库
    this.$refs.procDlg.show(this.tags.service.initTitle, this.tags.service.initAlert, 'run_circle',
        (dlg)=> {
            var opts={method:"get", url:"/initdb"};
            return this.service.request_private(opts, this.name);
        },
        (dlg,resp)=> {
          if(resp.code!=RetCode.OK) {
            dlg.setInfo(formatErr(resp.code, resp.info));
          } else {
            dlg.setInfo(this.tags.service.initSuccess);
            this.refeshSrvs(resp);
          }
        }
    )
},
showStats(){
    this.stats.dlg=true;
    this.stats.errMsg='';
    this.stats.chart=Vue.markRaw(echarts.init(document.getElementById('stats_chart')));
    var from=parseInt(new Date(this.stats.date.from).getTime()/HOUR_MS);
    var to=parseInt(new Date(this.stats.date.to).getTime()/HOUR_MS)
    var opts={method:"GET", url:"/stats/companyServiceStats?service="+this.name+"&from="+from+"&to="+to};
    this.service.request_cloud(opts, "appstore").then(resp=>{
        if(resp.code != RetCode.OK) {
            this.stats.errMsg=formatErr(resp.code, resp.info, '');
            return;
        }
        if(resp.data.stats.length==0) {
            return;
        }
        var dt=new Date();
        var cols=resp.data.cols;
        var cn=cols.length;
        var data={};
        var day;

        for(var l of resp.data.stats) {
            var d={};
            for(var i=0; i<cn; i++) {
                d[cols[i]]=l[i];
            }
            day=data[d.day]; //将多个service汇总
            if(!day) {
                day={day:d.day,apis:new Array(24).fill(0),fails:new Array(24).fill(0),excs:new Array(24).fill(0)};
                data[d.day]=day;
            }
            for(var h=0; h<24; h++) {
                var hd=d['h'+h];
                if(!hd) continue;
                var ss=hd.split(',');//"api,fail,exc",...
                day.apis[h]=parseInt(ss[0]);
                day.fails[h]=parseInt(ss[1]);
                day.excs[h]=parseInt(ss[2]);
            }
        }
        var xAxis=[];
        var apis=[];
        var fails=[];
        var excs=[];
        var n,t,oldDay=from;
        for(var k in data) {
            d = data[k];
            n=d.day-oldDay;
            if(n>1) {
                n=(n-1)*24;
                t=(oldDay+1)*DAY_MS;
                for(var i=0;i<n;i++,t+=HOUR_MS) {
                    dt.setTime(t);
                    apis.push(0);
                    fails.push(0);
                    excs.push(0);
                    xAxis.push(this.formatXAxis(dt));
                }                   
            }
            t=d.day*DAY_MS;
            for(var i=0;i<24;i++,t+=HOUR_MS) {
                dt.setTime(t);
                apis.push(d.apis[i]);
                fails.push(d.fails[i]);
                excs.push(d.excs[i]);
                xAxis.push(this.formatXAxis(dt));
            }
            oldDay=d.day;
        }
        var series=[
            {name:this.tags.service.requests, type:'bar', data:apis, yAxisIndex:0},
            {name:this.tags.service.excs, type:'line', data:excs, yAxisIndex:0, itemStyle:{color:'red'}},
            {name:this.tags.service.fails, type:'line', data:fails, yAxisIndex:0, itemStyle:{color:'orange'}}
        ];

        this.serviceStats.chart.setOption({
            title: {show:false},
            tooltip: {},
            legend: {type:'scroll', bottom:10, width:this.serviceStats.width},
            grid: {left:'0%', containLabel:true},
            xAxis: {data:xAxis, type:'category', axisLabel:{interval:(i,l)=>{return l.length>5}}},
            yAxis: [{name:this.tags.service.unit, minInterval:1}],
            series: series
        })
    })
},
formatXAxis(dt) {
    var h=dt.getHours();
    if(h==0) {
        return dt.getFullYear()+'-'+(dt.getMonth()+1)+'-'+dt.getDate();
    }
    return h+':00';
},
statsDateChanged() {
    if(this.stats.proxyDate) {
        this.stats.date=this.stats.proxyDate;
        this.showStats();
    }
},
rangeFilter(dt) {
    var now=Date.now();
    var t=Date.parse(dt);
    return t<=now&&t>=now-365*24*HOUR_MS;
},
clear_service() {
    this.$refs.confirmDlg.show(this.tags.om.advRmvService, ()=>{
        var opts={method:"DELETE",url:"/service/remove?service="+this.name};
        this.service.request_private(opts, "bios").then(resp=>{
            if(resp.code != RetCode.OK) {
                this.$refs.errDlg.showErr(resp.code, resp.info);
                return;
            }
            this.service.go_back();
        })
    })
}
},
template:`
<q-layout view="hHh lpr fFf">
 <q-header class="bg-grey-1 text-primary">
  <q-toolbar>
   <q-btn flat round icon="arrow_back" dense @click="service.go_back"></q-btn>
   <q-toolbar-title>{{name}}{{tags.detailInfo}}</q-toolbar-title>
   <q-btn flat round icon="bar_chart" dense @click="stats.dlg=true"></q-btn>
  </q-toolbar>
 </q-header>

 <q-page-container>
   <q-page class="q-pa-md">
<q-banner rounded class="bg-grey-3 text-h5" dense>{{tags.service.keypair}}</q-banner>
<div style="max-width:98vw;overflow-wrap:break-word;word-break:normal;white-space:normal;">{{key}}
 <q-popup-edit v-model="key" v-slot="scope" @update:model-value="set_key"
  buttons :label-set="tags.ok" :label-cancel="tags.cancel" auto-save ref="dlg_set_key">
  <q-input v-model="scope.value" dense autofocus @keyup.enter="scope.set" type="text"></q-input>
 </q-popup-edit>
</div>

<q-banner rounded class="bg-grey-3 text-h5 q-mt-lg" dense inline-actions>{{tags.service.db}}
 <template v-slot:action>
  <q-btn flat dense :label="dbNo">
   <q-popup-edit v-model="dbNo" v-slot="scope" @update:model-value="set_dbNo"
   buttons :label-set="tags.ok" :label-cancel="tags.cancel" auto-save ref="dlg_set_dbNo">
   <q-input v-model="scope.value" dense autofocus @keyup.enter="scope.set" type="text"></q-input>
   </q-popup-edit>
  </q-btn>
  <q-btn text-color="primary" icon="history" flat dense @click="initDbs"></q-btn>
 </template>
</q-banner>

<q-list>
 <q-item v-for="db in dbList">
  <q-item-section>{{db.name}}</q-item-section>
  <q-item-section avatar><q-chip color="green" text-color="white" :icon="db.type">{{db.sType}}</q-chip></q-item-section>
 </q-item>
</q-list>

<q-banner rounded class="bg-grey-3 text-h5 q-mt-lg" dense inline-actions>{{tags.service.caller}}
 <template v-slot:action>
  <q-btn text-color="primary" icon="add_circle" flat dense>
   <q-popup-proxy ref="dlg_add_caller">
    <q-card style="min-width:30vw;">
     <q-card-section>
      <component-service-selector :label="tags.caller" :services="caller.name" :multi="false" :useid="false"></component-service-selector>
      <q-input v-model="caller.features" :label="tags.features"></q-input>
     </q-card-section>
     <q-card-section align="right">
      <q-btn :label="tags.ok" color="primary" @click="add_caller"></q-btn>
      <q-btn flat :label="tags.cancel" color="primary" v-close-popup></q-btn>
     </q-card-section>
    </q-card>
   </q-popup-proxy>
  </q-btn>
 </template>
</q-banner>
<q-list>
 <q-item v-for="c in caller.list">
  <q-item-section>{{c.name}}</q-item-section>
  <q-item-section>{{c.val}}</q-item-section>
  <q-item-section avatar @click="remove_caller(c.name)">
   <q-icon color="primary" text-color="white" name="delete"></q-icon>
  </q-item-section>
 </q-item>
</q-list>

<q-banner rounded class="bg-grey-3 text-h5 q-mt-lg" dense inline-actions>{{tags.service.configs}}
 <template v-slot:action>
  <q-btn text-color="primary" icon="add_circle" flat dense>
   <q-popup-proxy ref="dlg_add_config">
    <q-card style="min-width:30vw;">
     <q-card-section>
      <q-input v-model="config.name" :label="tags.configKey"></q-input>
      <q-input v-model="config.val" :label="tags.configVal"></q-input>
     </q-card-section>
     <q-card-section align="right">
      <q-btn :label="tags.ok" color="primary" @click="add_config"></q-btn>
      <q-btn flat :label="tags.cancel" color="primary" v-close-popup></q-btn>
     </q-card-section>
    </q-card>
   </q-popup-proxy>
  </q-btn>
 </template>
</q-banner>
<q-list>
 <q-item v-for="(v,k) in config.list">
  <q-item-section>{{k}}</q-item-section>
  <q-item-section>{{v}}</q-item-section>
  <q-item-section avatar>
   <q-icon color="primary" text-color="white" name="delete" @click="remove_config(k)"></q-icon>
  </q-item-section>
 </q-item>
</q-list>

<q-banner rounded class="bg-grey-3 text-h5 q-mt-lg" dense inline-actions>{{tags.om.srvNodes}}
</q-banner>
<q-list dense>
 <q-item v-for="n in nodes">
  <q-item-section>{{n.addr}}</q-item-section>
  <q-item-section>{{n.partId}}</q-item-section>
  <q-item-section>{{n.status}}</q-item-section>
  <q-item-section>{{n.ver}}</q-item-section>
 </q-item>
</q-list>

    </q-page>
  </q-page-container>
</q-layout>
<component-process-dialog ref="procDlg"></component-process-dialog>
<component-alert-dialog ref="errDlg" :title="tags.failToCall" :close="tags.close"></component-alert-dialog>
<component-confirm-dialog :title="tags.alert" :close="tags.cancel" :ok="tags.ok" ref="confirmDlg"></component-confirm-dialog>

<!-- 请求统计弹窗 -->
<q-dialog v-model="stats.dlg" no-backdrop-dismiss @show="showStats">
 <q-card style="min-width:80vw;">
  <q-card-section class="row items-center q-pb-none">
   <div>
    <div class="text-h6">{{tags.service.requests}}</div>
    <div class="text-caption text-grey">{{stats.date.from}} => {{stats.date.to}}</div>
   </div>
   <q-space></q-space>
   <q-btn icon="event" flat>
    <q-popup-proxy cover transition-show="scale" transition-hide="scale">
     <q-date v-model="stats.proxyDate" range :options="rangeFilter">
      <div class="row items-center justify-end">
       <q-btn :label="tags.ok" color="primary" @click="statsDateChanged" v-close-popup></q-btn>
       <q-btn :label="tags.close" color="primary" flat v-close-popup></q-btn>
      </div>
     </q-date>
    </q-popup-proxy>
   </q-btn>
   <q-btn icon="close" flat round dense v-close-popup></q-btn>
  </q-card-section>
  <q-card-section class="q-pt-none">
    <div id="stats_chart" style="width:78vw;height:70vh;"
     class="flex justify-center items-center">{{stats.errMsg}}</div>
  </q-card-section>
 </q-card>
</q-dialog>
`}