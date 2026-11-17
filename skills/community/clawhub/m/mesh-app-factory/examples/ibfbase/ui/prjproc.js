import AlertDialog from "/assets/v3/components/alert_dialog.js"
import MonthInput from "/assets/v3/components/month_input.js"
import SkuSelector from "./components/sku_selector.js"
import UserInput from "/assets/v3/components/user_input.js"
import DateInput from "/assets/v3/components/date_input.js"
import {sta2icon} from '/assets/v3/components/workflow.js';

const EMPTY_PUR={expDate:'',descr:'',type:'SELF',receiver:'',buyer:[]};
const RT_TAB="prjproc_tab";
const BALANCE_TYPES = "prj_bal_types";

export default {
inject:["ibf"],
components:{
    "alert-dialog":AlertDialog,
    "month-input":MonthInput,
    "date-input":DateInput,
    "sku-select":SkuSelector,
    "user-input":UserInput
},
data() {return {
    pid:this.$route.query.id,
    prj:{}, //项目详情
    wts:[],
    purs:[],
    busis:[],
    bals:[],
    editable:false, //项目是否可编辑
    over:false, //是否结束
    isLeader:false,
    tags:this.ibf.tags,
    tab:'', //worktime,busi,purchase
    balCharts:null,

    wt:{cur:1,max:0,dlg:false,month:'-1m',no:-1}, //按月查询工时申请
    busi:{cur:1,max:0},
    purchase:{cur:1,max:0,dlg:false,typeOpts:[],
        dta:{},skus:[],sku:{sku:{},num:''}},
    bal:{month:{year:0,month:1},monNum:12,typeDlg:false,types:[],chged:false,
        x:[],series:[]}
}},
created(){
    var types=storageGet(BALANCE_TYPES,'["salary","income","pay"]');
    this.bal.types=JSON.parse(types);

    request({method:'GET',url:'/project/detail?id='+this.pid}, this.ibf.SERVICE_PRJ).then(resp => {
        if(resp.code!=RetCode.OK) {
            return;
        }
        this.prj=resp.data;
        var dt=new Date();
        dt.setTime(this.prj.start*60000);
        this.prj.start_s=date2str(dt); //用于输入计划时限制时间范围
        dt.setTime(this.prj.end*60000);
        this.prj.end_s=date2str(dt);
        this.isLeader=this.prj.role=='L';
        var stage=this.prj.stage;
        var stageDef=this.ibf.PrjStage;
        this.editable=this.isLeader&&stage==stageDef.init;
        this.over=stage==stageDef.end||stage==stageDef.cancel;
        this.tab=this.ibf.getRt(RT_TAB,'worktime');
        this.tab_changed(this.tab);
    });
    var tps=this.tags.purchase.types;
    for(var t in tps) {
        this.purchase.typeOpts.push({value:t, label:tps[t]});
    }
},
mounted(){ //mounted在created之后
loadJs("/assets/v3/echarts.js").then(r=>{
    if(!r) Console.info("fail to load echarts"); 
})
},
methods:{
tab_changed(tab) {
    this.ibf.setRt(RT_TAB, tab);
    if(tab=='worktime'){
        if(this.wts.length==0) {
            this.query_wts(this.wt.cur);
        }
    } else if(tab=='purchase'){
        if(this.purs.length==0) {
            this.query_purchase(this.purchase.cur);
        }
    } else if(tab=='bal'){
        if(this.bals.length==0) {
            this.query_bal();
        }
    } else {
        if(this.busis.length==0) {
            this.query_busi(this.busi.cur);
        }
    }
},
query_busi(pg) {
    var offset=(parseInt(pg)-1)*this.ibf.N_PAGE;
    var opts={method:"GET", url:"/business/listbypid?pid="
        +this.pid+"&offset="+offset+'&num='+this.ibf.N_PAGE}
    request(opts, this.ibf.SERVICE_BUSINESS).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.busis=[];
            this.busi.max=0;
            this.busi.cur=1;
            return;
        }
        //id,prjName,flowid,status,start,end,
        //expense,subsidy,dest,account,reason
        var dt=new Date();
        var busi=[];
        for(var l of resp.data.list) {
            var b={};
            var i=0;
            for(var c of resp.data.cols) {
                b[c]=l[i++];
            }
            dt.setTime(b.start*60000);
            b.start_s=date2str(dt);
            dt.setTime(b.end*60000);
            b.end_s=date2str(dt);
            busi.push(b);
        }
        this.busi.max=Math.ceil(resp.data.total/this.ibf.N_PAGE);
        this.busis=busi;
    })
},
query_wts(pg) {
    if(!this.wt.month.num)return;//第一次切换到此tab，month还没准备好
    var offset=(parseInt(pg)-1)*this.ibf.N_PAGE;
    var url="/tasktime/wait?pid="+this.pid
            +"&offset="+offset+'&num='+this.ibf.N_PAGE
            +"&month="+this.wt.month.num
    request({method:"GET", url:url}, this.ibf.SERVICE_HR).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.wts=[];
            this.wt.max=0;
            return;
        }
        this.wts=resp.data.list.map(l=>{
            l.state_s=this.tags.aplSta[l.state];
            return l;
        });
        this.wt.max=Math.ceil(resp.data.total/this.ibf.N_PAGE);
    })
},
query_purchase(pg) {
    var offset=(parseInt(pg)-1)*this.ibf.N_PAGE;
    var opts={method:"GET", url:"/purchase/listByPid?pid="
        +this.pid+"&offset="+offset+'&num='+this.ibf.N_PAGE}
    request(opts, this.ibf.SERVICE_RES).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.purs=[];
            this.purchase.max=0;
            this.purchase.cur=1;
            return;
        }
        //id,cost,expDate,status,flowid,applicant,
        //receiver,descr,pid,prjName
        var dt=new Date();
        this.purs=resp.data.list.map(b => {
            dt.setTime(b.expDate*60000);
            b.expDate=date2str(dt);
            b.status=sta2icon(b.status);
            b.type=this.tags.purchase.types[b.type];
            return b;
        });
        this.purchase.max=Math.ceil(resp.data.total/this.ibf.N_PAGE);
    })
},
query_bal() {
    if(!this.bal.month.num) return;
    var end=this.bal.month.num;
    var start=end-this.bal.monNum;
    var dta={start:start, end:end, pid:this.pid, types:this.bal.types};
    request({method:"POST",url:"/project/report", data:dta},this.ibf.SERVICE_FINANCE).then(resp=>{
        if(resp.code!=RetCode.OK) {
            resp.data={snapshots:[]}
        }
        var m,sm;
        var monNum=this.bal.monNum;
        var bals=new Array(monNum); //按月分行，每行记录多个类型
        var xAxis=[];
        var bal;
        for(var i=0;i<monNum;i++) {
            m=i+start+1;
            sm=parseInt(m/12)+'/'+((m%12)+1);
            bal={month:sm};
            for(var type in this.bal.types) bal[type]=0;
            bals[monNum-i-1]=bal; //倒序
            xAxis.push(sm);
        }
        this.bal.x=xAxis;
    
        var bals1={}; //按类型分行，每行n个月
        for(var type of this.bal.types) {//每个类型填充0
            bals1[type]=new Array(monNum).fill(0);
        }
    
        var v;
        resp.data.snapshots.map(l => { //向bals中填充实际值，没有的保持0值
            m=l.month-start-1;
            for(var tp of this.bal.types) {
                v=l[tp].toFixed(2);
                bals[monNum-m-1][tp]=v;
                bals1[tp][m]=v;
            }
        })
        this.bals=bals;
        
        var series=[];
        for(var type in bals1) {
            series.push({name:this.tags.bal.types[type],type:'line',data:bals1[type]});
        }
        this.bal.series=series;
        this.show_chart();
    })
},
show_chart() {
    this.balCharts=Vue.markRaw(echarts.init(document.getElementById('balCharts')));
    this.balCharts.setOption({
        title: {show:false},
        tooltip: {},
        grid: {left:'0%',containLabel:true},
        legend: {type:'scroll',bottom:10,width:this.ibf.CLIENTW-60},
        xAxis: {data:this.bal.x},
        yAxis: [{name:this.tags.bal.val}],
        series: this.bal.series
    });
},
set_types() {
    if(this.bal.chged) {
        var types=this.bal.types.filter(tp=>{
            return this.tags.bal.types[tp];
        })
        this.bal.types=types;
        storageSet(BALANCE_TYPES, JSON.stringify(types));
        this.bal.chged=false;
        this.query_bal();
    }
},
purchase_sta_changed() {
    this.query_purchase(this.purchase.cur);
},
month_changed() {
    this.wt.cur=1;
    this.query_wts(1);
},
show_wt(no) {
    this.wt.no=no;
    this.wt.dlg=true;
},
wt_do(state) {
    if(this.wt.no<0)return;
    var uid=this.wts[this.wt.no].uid;
    var dta={pid:this.pid,uid:uid,month:this.wt.month.num,state:state};
    request({method:'POST',url:'/tasktime/confirm', data:dta}, this.ibf.SERVICE_HR).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.$refs.alertDlg.showErr(resp.code, resp.info);
            return;
        }
        this.query_wts(this.wt.cur);
        this.wt.no=-1;
        this.wt.dlg=false;
    });
},
show_purchase() {
    copyObjTo(EMPTY_PUR, this.purchase.dta);
    this.purchase.skus=[];
    this.purchase.sku={sku:{id:0,name:''},num:''};
    this.purchase.dlg=true;
},
purchase_do() {
    var pur=this.purchase.dta;
    var dta=copyObj(pur, ['receiver','type','descr']);
    dta.pid=this.pid;
    dta.prjName=this.prj.name;
    dta.expDate=parseInt(Date.parse(pur.expDate)/60000);
    dta.buyer=pur.buyer.account;
    dta.skus=this.purchase.skus;
    request({method:"POST", url:"/purchase/apply", data:dta}, this.ibf.SERVICE_RES).then(resp=>{
        if(resp.code != RetCode.OK) {
            this.$refs.alertDlg.showErr(resp.code, resp.info);
            return;
        }
        this.purchase.dlg=false;
        this.query_purchase(this.purchase.cur);
    });
},
add_purchase_sku() {
    var sku=this.purchase.sku.sku;
    var num=this.purchase.sku.num;
    if(sku.id==0 || !num)return;
    this.purchase.skus.push({sku:sku.id,skuName:sku.name,num:num});
    sku={id:0,name:''};
    this.purchase.sku.num='';
},
rmv_purchase_sku(i){
    this.purchase.skus.splice(i,1);
},
busi_flow(flowid,did) {
    this.ibf.showFlow(flowid,did,'/ibf/workflow?service='+this.ibf.SERVICE_BUSINESS) 
}
},
template:`
<q-layout view="hHh lpr fFf">
  <q-header>
   <q-toolbar>
     <q-btn flat icon="arrow_back" dense @click="ibf.back()"></q-btn>
     <q-toolbar-title>{{tags.prj.title}}-{{prj.name}}</q-toolbar-title>
     <q-btn flat dense icon="info" @click.stop="ibf.goto('/ibf/prjinfo?id='+pid)"></q-btn>
   </q-toolbar>
  </q-header>
  <q-footer>
   <q-tabs v-model="tab" @update:model-value="tab_changed"
    dense align="justify" switch-indicator inline-label
    class="text-grey bg-grey-3" active-color="primary" indicator-color="primary">
    <q-tab name="worktime" icon="work_history" :label="tags.prj.worktime"></q-tab>
    <q-tab name="busi" icon="business" :label="tags.busi.title"></q-tab>
    <q-tab name="purchase" icon="shopping_cart" :label="tags.purchase.title"></q-tab>
    <q-tab name="bal" icon="trending_up" :label="tags.bal.title"></q-tab>
   </q-tabs>
  </q-footer>
  <q-page-container>
    <q-page class="q-pa-none">
<q-tab-panels v-model="tab">

<q-tab-panel name="busi">
 <q-list dense separator>
  <q-item v-for="(b,i) in busis" @click="busi_flow(b.flowid,b.id)" clickable>
   <q-item-section>
    <q-item-label>{{b.account}}</q-item-label>
    <q-item-label caption>{{b.dest}}</q-item-label>
   </q-item-section>
   <q-item-section>
    <q-item-label>{{b.reason}}</q-item-label>
    <q-item-label caption>{{b.start_s}}-&gt;{{b.end_s}}</q-item-label>
   </q-item-section>
   <q-item-section side>
    <q-item-label>{{tags.busi.expense}}:{{b.expense}}</q-item-label>
    <q-item-label>{{tags.busi.subsidy}}:{{b.subsidy}}</q-item-label>
   </q-item-section>
  </q-item>
 </q-list>
 <div class="q-pa-sm flex flex-center" v-show="busi.max>1">
  <q-pagination v-model="busi.cur" color="primary" :max="busi.max" max-pages="10"
   boundary-numbers="false" @update:model-value="query_busi"></q-pagination>
 </div>
</q-tab-panel>

<q-tab-panel name="worktime">
 <month-input v-model="wt.month" min="-3" max="-1m"
   class="justify-center text-primary"
   @update:modelValue="month_changed"></month-input>
 <div class="q-pa-sm flex flex-center" v-show="wt.max>1">
  <q-pagination v-model="wt.cur" color="primary" :max="wt.max" max-pages="10"
   boundary-numbers="false" @update:model-value="query_wts"></q-pagination>
 </div>
 <q-list dense separator>
  <q-item v-for="(l,i) in wts" @click="show_wt(i)" clickable>
   <q-item-section>{{l.account}}</q-item-section>
   <q-item-section>
    <q-item-label>{{l.ratio}}%({{l.state_s}})</q-item-label>
    <q-item-label caption>{{l.cmt}}</q-item-label>
   </q-item-section>
  </q-item>
 </q-list>
</q-tab-panel>

<q-tab-panel name="purchase" class="q-pa-none">
 <div class="bg-grey-3 q-pa-sm text-right" v-if="!over">
   <q-btn color="primary" @click="show_purchase" icon="add_shopping_cart" flat dense></q-btn>
 </div>
 <div class="q-pa-sm flex flex-center" v-show="purchase.max>1">
  <q-pagination v-model="purchase.cur" color="primary" :max="purchase.max" max-pages="10"
   boundary-numbers="false" @update:model-value="query_purchase"></q-pagination>
 </div>
 <q-list dense separator class="q-pa-sm">
  <q-item v-for="(l,i) in purs" @click="ibf.goto('/ibf/purchasedtl?id='+l.id)" clickable>
   <q-item-section>
    <q-item-label>{{l.applicant}}</q-item-label>
    <q-item-label caption>{{l.expDate}}</q-item-label>
   </q-item-section>
   <q-item-section>
    <q-item-label>{{l.receiver}}</q-item-label>
    <q-item-label caption>{{l.descr}}</q-item-label>
   </q-item-section>
   <q-item-section side>
    <q-item-label>{{l.cost}} {{tags.currency}}</q-item-label>
    <q-item-label caption>{{l.type}}</q-item-label>
   </q-item-section>
  </q-item>
 </q-list>
</q-tab-panel>

<q-tab-panel name="bal" class="q-pa-none">
 <div class="row q-pa-md">
  <div class="col text-primary">
   <month-input class="text-subtitle1 q-pl-sm" v-model="bal.month"
   @update:modelValue="query_bal()" min="-10y" max="cur"></month-input>
  </div>
  <div class="col text-right">
   <q-btn flat icon="list" dense @click="bal.typeDlg=true" color="primary"></q-btn>
  </div>
 </div>
 <div id="balCharts" :style="{width:'99vw', height:'35vh'}"></div>
 <q-markup-table flat dense>
  <thead>
   <tr>
    <th></th>
    <th v-for="i in bal.types">{{tags.bal.types[i]}}</th>
   </tr>
  </thead>
  <tbody>
    <tr v-for="l in bals">
     <td class="text-left">{{l.month}}</td>
     <td class="text-center" v-for="i in bal.types">{{l[i]}}</td>
    </tr>
  </tbody>
 </q-markup-table>
</q-tab-panel>

</q-tab-panels>
    </q-page>
  </q-page-container>
</q-layout>

<q-dialog v-model="wt.dlg" position="right">
<q-card style="width:6em;">
 <q-card-section class="text-center">
  <div class="q-pb-lg">
   <q-btn icon="thumb_up" :label="Stacked" stack flat color="primary"
   @click="wt_do('OK')"></q-btn>
  </div>
  <div>
   <q-btn icon="thumb_down" :label="Stacked" stack flat color="red"
   @click="wt_do('REJ')"></q-btn>
  </div>
 </q-card-section>
</q-card>
</q-dialog>

<q-dialog v-model="purchase.dlg">
<q-card style="min-width:70vw">
 <q-card-section>
  <div class="text-h6">{{tags.apply}}</div>
 </q-card-section>
 <q-card-section class="q-pt-none">
  <q-select v-model="purchase.dta.type" :options="purchase.typeOpts"
   dense map-options emit-value></q-select>
  <q-input v-model="purchase.dta.receiver" dense
   :label="tags.purchase.receiver"></q-input>
  <date-input v-model="purchase.dta.expDate" :format="tags.dateFmt"
  :label="tags.purchase.expDate" min="today"></date-input>
  <user-input v-model="purchase.dta.buyer" :label="tags.purchase.buyer"></user-input>
  <q-input v-model="purchase.dta.descr" :label="tags.cmt" dense></q-input>
  <q-banner inline-actions class="bg-indigo-1 q-mt-sm" dense>
    {{tags.purchase.skuList}}
  </q-banner>
  <q-list>
   <q-item clickable v-for="(s,i) in purchase.skus">
    <q-item-section>{{s.skuName}}</q-item-section>
    <q-item-section>{{s.num}}</q-item-section>
    <q-item-section side>
     <q-icon color="red" name="clear" @click="rmv_purchase_sku(i)"></q-icon>
    </q-item-section>
   </q-item>
   <q-item>
    <q-item-section>
     <sku-select v-model="purchase.sku.sku" :label="tags.purchase.sku"></sku-select>
    </q-item-section>
    <q-item-section>
     <q-input v-model.number="purchase.sku.num" :label="tags.num" dense></q-input>
    </q-item-section>
    <q-item-section side>
     <q-icon name="add_circle" @click="add_purchase_sku" color="primary"></q-icon>
    </q-item-section>
   </q-item>
  </q-list>
 </q-card-section>
 <q-card-actions align="right">
   <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
   <q-btn :label="tags.ok" color="primary" @click="purchase_do"></q-btn>
 </q-card-actions>
</q-card>
</q-dialog>

<q-dialog v-model="bal.typeDlg" position="top" @hide="set_types">
 <q-card style="width:100vw">
  <q-card-section>
   <div class="q-gutter-sm">
     <q-checkbox v-for="(l,tp) in tags.bal.types" @update:model-value="bal.chged=true"
      v-model="bal.types" :val="tp" :label="l"></q-checkbox>
   </div>
  </q-card-section>
 </q-card>
</q-dialog>

<alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" ref="alertDlg"></alert-dialog>
`
}