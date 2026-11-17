import AlertDialog from "/assets/v3/components/alert_dialog.js";
import DatetimeInput from "/assets/v3/components/datetime_input.js";
import PrjInput from "./components/prj_selector.js";
import {datetimeToStr, datetimeToDate} from '/assets/v3/components/datetime_input.js';
const HOLIDIES=['AFFA','SICK','WEAL','HOLI'];
const OTWS=['WOW','OOW','FOW','OTW'];
const EMPTY_TM={type:'OTW',start:'',end:'',cmt:''};
const EMPTY_WT={prj:{},ratio:'',cmt:'',editable:true};

export default {
inject:["ibf"],
components:{
    "alert-dialog" : AlertDialog,
    "datetime-input":DatetimeInput,
    "prj-input":PrjInput
},
data() {return {
    tags:this.ibf.tags,
    tab:'atd', //exp(考勤异常),atd(加班请假),wt(worktime工时申报)
    atds:[], //请假或加班申请记录
    exps:[], //考勤异常记录
    wts:[], //工时申报
    atdPg:{max:0,cur:1},
    wtPg:{max:0,cur:1},
    atdAct:{dlg:false,no:-1,dta:{},tms:[],tm:{},editable:true},
    wtAct:{dlg:false,no:-1,items:[],wt:{}, month:'',editable:true},
    expAct:{dlg:false,no:-1,dta:{}},
    tmTypes:[]
}},
created(){
    this.query_atds();
    this.tmTypes.push({value:'OTW',label:this.tags.atd.ovt});
    for(var i of ['BUSI','AFFA','SICK','WEAL','HOLI']) {
        this.tmTypes.push({value:i,label:this.tags.atd.aplTmType[i]});
    }
},
methods:{
tab_changed(tab) {
    if(tab=='exp') {
        if(this.exps.length==0) {
            this.query_exps();
        }
    } else if(tab=='wt') {
        if(this.wts.length==0) {
            this.query_wts(this.wtPg.cur);
        }
    } else {
        if(this.atds.length==0) {
            this.query_atds(1);
        }
    }
},
query_exps() {
    request({method:"GET", url:"/exception/my"}, this.ibf.SERVICE_HR).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.exps=[];
            return;
        }
        //day,state,start,end,realStart,realEnd,cfmAcc,descr
        var dt=new Date();
        this.exps=resp.data.list.map(e=>{
            dt.setTime(e.day*86400000);
            var d=e.day%10000;
            var m=parseInt(d/100);
            d=d%100;
            e.day_s=parseInt(e.day/10000)+'/'+(m<10?('0'+m):m)+'/'+(d<10?('0'+d):d);
            e.start_s=this.expdt2str(e.start,dt);
            e.end_s=this.expdt2str(e.end,dt);
            e.realStart_s=this.expdt2str(e.realStart,dt);
            e.realEnd_s=this.expdt2str(e.realEnd,dt);
            e.state_s=this.tags.aplSta[e.state];
            return e;
        });
    })
},
query_wts(pg) {
    var offset=(parseInt(pg)-1)*this.ibf.N_PAGE;
    var url="/tasktime/my?offset="+offset+'&num='+this.ibf.N_PAGE;
    request({method:"GET", url:url}, this.ibf.SERVICE_HR).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.wts=[];
            return;
        }
        //month,pid,prjName,cfmAcc,cmt,state,ratio,at
        var dt=new Date();
        this.wts=resp.data.list.map(a=>{
            a.state_s=this.tags.aplSta[a.state];
            dt.setTime(a.at);
            a.at=datetime2str(dt,true);
            var mon=(a.month%12) + 1;
            a.month_s=parseInt(a.month/12)+'/'+(mon>10?mon:'0'+mon);
            return a;
        });
        this.wtPg.max=Math.ceil(resp.data.total/this.ibf.N_PAGE);
    })
},
query_atds(pg) {
    var offset=(parseInt(pg)-1)*this.ibf.N_PAGE;
    var url="/apply/myAtdApplies?offset="+offset+'&num='+this.ibf.N_PAGE;
    request({method:"GET", url:url}, this.ibf.SERVICE_HR).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.atds=[];
            return;
        }
        var dt=new Date();
        //id,uid,type,state,opinion,at
        this.atds=resp.data.list.map(a=>{
            a.type_s=this.tags.atd.aplType[a.type];
            a.state_s=this.tags.aplSta[a.state];
            a.editable=a.state!='OK';
            dt.setTime(a.at);
            a.at=datetime2str(dt,true);
            return a;
        });
        this.atdPg.max=Math.ceil(resp.data.total/this.ibf.N_PAGE);
    })
},
get_atd_dtl(aid,no) {
    var url="/attendance/getApply?id="+aid;
    request({method:"GET", url:url}, this.ibf.SERVICE_HR).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.atdAct.tms=[];
            this.atdAct.dta={};
            this.$refs.alertDlg.showErr(resp.code, resp.info);
            return
        }
        var dt=new Date();
        //type,start,end,cmt
        this.atdAct.tms=resp.data.times.map(a=>{
            a.type_s=this.tags.atd.aplTmType[a.type];
            dt.setTime(a.start*60000);
            a.start_s=datetime2str(dt);
            dt.setTime(a.end*60000);
            a.end_s=datetime2str(dt);
            a.state_s=this.tags.aplSta[a.state];
            return a;
        });
        this.atdAct.dta=resp.data;
        this.atdAct.dta.id=aid;
        this.atdAct.editable=this.atdAct.dta.state!='OK';
        this.atdAct.no=no;
        this.atdAct.dlg=true;
    });
},
show_add() {
    if(this.tab=='atd') {
        this.show_atd(-1);
    } else {
        this.show_wt(-1);
    }
},
show_atd(no) {
    copyObjTo(EMPTY_TM, this.atdAct.tm);
    if(no>-1) {
        this.get_atd_dtl(this.atds[no].id,no);
    } else {
        this.atdAct.no=-1;
        this.atdAct.tms=[];
        this.atdAct.dlg=true;
        this.atdAct.editable=true;
    }
},
add_atd_tm() {
    var tm=copyObj(this.atdAct.tm, ['type','cmt']);
    var dt=datetimeToDate(this.atdAct.tm.start);
    if(tm.type=='OTW') {
        tm.type_s=this.tags.atd.ovt;
    } else {
        tm.type_s=this.tags.atd.aplTmType[tm.type];
    }
    for(var t of this.atdAct.tms) {
        if(t.type==tm.type) {//同一次请求，必须是同类的
            continue;
        }
        if(tm.type=='OTW') {
            if(OTWS.indexOf(t.type)<0) {
                this.$refs.alertDlg.show(this.tags.onlyOneType);
                return;
            }
        } else if(HOLIDIES.indexOf(tm.type)>=0) {
            if(HOLIDIES.indexOf(t.type)<0) {
                this.$refs.alertDlg.show(this.tags.onlyOneType);
                return;
            }
        }
    }
    tm.start=parseInt(dt.getTime()/60000);
    tm.start_s=datetimeToStr(this.atdAct.tm.start,this.tags.dateFmt);
    dt=datetimeToDate(this.atdAct.tm.end);
    tm.end=parseInt(dt.getTime()/60000);
    tm.end_s=datetimeToStr(this.atdAct.tm.end,this.tags.dateFmt);
    if(tm.start>=tm.end) {
        this.$refs.alertDlg.show(this.tags.invalidInterval);
        return;
    }
    this.atdAct.tms.push(tm);
    if(this.hasOverlap(this.atdAct.tms)) {
        this.atdAct.tms.pop();
        this.$refs.alertDlg.show(this.tags.hasOverlap);
    } else {
        copyObjTo(EMPTY_TM, this.atdAct.tm);
    }
},
rmv_atd_tm(i) {
    this.atdAct.tms.splice(i,1);
},
atd_do() { //加班、请假或工作日在途
    if(this.atdAct.tms.length==0) {
        return;
    }
    var tms=[];
    for(var tm of this.atdAct.tms) {
        tms.push(copyObj(tm,['type','cmt','start','end']));
    }
    var dta={times:tms};
    var tp=this.atdAct.tms[0].type;
    
    var url="/attendance/";
    if(OTWS.indexOf(tp)>=0) url+='overtimework';
    else if(tp=='BUSI') url+='onBusiness';
    else url+="leave";
    
    if(this.atdAct.no>-1) { //修改
        dta.id=this.atdAct.dta.id;
    }
    request({method:"POST", url:url, data:dta}, this.ibf.SERVICE_HR).then(resp => {
        if(resp.code != RetCode.OK) {
            this.$refs.alertDlg.showErr(resp.code, resp.info);
            return;
        }
        this.atdAct.dlg=false;
        this.atdAct.no=-1;
        this.query_atds(this.atdPg.cur);
    });
},
remove_atd() {
    if(this.atdAct.no<0) return;
    var opts={method:"DELETE",url:"/attendance/cancel?id="+this.atdAct.dta.id};
    request(opts, this.ibf.SERVICE_HR).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.$refs.alertDlg.showErr(resp.code, resp.info);
            return;
        }
        this.atdAct.dlg=false;
        this.atdAct.no=-1;
        this.query_atds(this.atdPg.cur);
    });
},
get_wt_dtl(month,no) {
    var url="/tasktime/getApply?month="+month;
    request({method:"GET", url:url}, this.ibf.SERVICE_HR).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.wtAct.items=[];
            this.$refs.alertDlg.showErr(resp.code, resp.info);
            return
        }
        
        var editableNum=0;
        //month,ratio,state,pid,prjName,cfmAcc,cmt
        if(resp.data.items.length>0) {
            var mon = (month%12) + 1;
            this.wtAct.month=parseInt(month/12)+'/'+(mon<10?('0'+mon):mon);
            this.wtAct.items=resp.data.items.map(a=>{
                if(a.state!='OK') {
                    editableNum++;
                }
                a.state_s=a.state_s=this.tags.aplSta[a.state];
                return a;
            })
        } else {
            editableNum=1;
            this.wtAct.items=[];
        }
        this.wtAct.editable=editableNum>0;
        this.wtAct.no=no;
        this.wtAct.dlg=true;
    });
},
show_wt(no) {
    copyObjTo(EMPTY_WT, this.wtAct.wt);
    if(no>-1) {
        this.get_wt_dtl(this.wts[no].month,no);
    } else {
        this.wtAct.no=-1;
        this.wtAct.items=[];
        this.wtAct.dlg=true;
        this.wtAct.editable=true;
        var dt=new Date();
        var n=dt.getMonth() + dt.getFullYear()*12 - 1; //增加上月的
        var mon=(n%12)+1;
        this.wtAct.month=parseInt(n/12)+'/'+(mon<10?('0'+mon):mon);
    }
},
add_wt_item() {
    if(!this.wtAct.wt.prj.id) {
        this.$refs.alertDlg.show(this.tags.plsInputPrj);
        return;
    }
    if(this.wtAct.wt.ratio<=0||this.wtAct.wt.ratio>100) {
        this.$refs.alertDlg.show(this.tags.invalidRatio);
        return;
    }
    var wt=copyObj(this.wtAct.wt, ['ratio','cmt']);
    wt.pid=this.wtAct.wt.prj.id;
    wt.prjName=this.wtAct.wt.prj.name;
    wt.editable=true;
    this.wtAct.items.push(wt);
    copyObjTo(EMPTY_WT, this.wtAct.wt);
},
rmv_wt_item(i) {
    this.wtAct.items.splice(i,1);
},
wt_declare() { //工时申报
    if(this.wtAct.items.length==0) {
        return;
    }
    var total=0;
    for(var item of this.wtAct.items) {
        total+=item.ratio;
    }
    if(total != 100) {
        this.$refs.alertDlg.show(this.tags.invalidRatio);
        return;
    }
    
    //[{pid,prjName,ratio,cmt},...]
    var dta={list:this.wtAct.items, month:this.wtAct.month.num};
    var opts={method:"POST", url:"/tasktime/declare", data:dta}
    request(opts, this.ibf.SERVICE_HR).then(resp => {
        if(resp.code != RetCode.OK) {
            this.$refs.alertDlg.showErr(resp.code, resp.info);
            return;
        }
        this.wtAct.dlg=false;
        this.wtAct.no=-1;
        this.query_wts(this.wtPg.cur);
    });
},
show_exp(no) {
    var dt=new Date();
    copyObjTo(this.exps[no], this.expAct.dta);
    if(this.expAct.dta.realStart<=0) {
        this.expAct.dta.realStart_s=this.expAct.dta.day_s;
    } else {
        dt.setTime(this.expAct.dta.realStart*60000);
        this.expAct.dta.realStart_s=datetime2str(dt);
    }
    if(this.expAct.dta.realEnd<=0) {
        this.expAct.dta.realEnd_s=this.expAct.dta.day_s;
    } else {
        dt.setTime(this.expAct.dta.realEnd*60000);
        this.expAct.dta.realEnd_s=datetime2str(dt);
    }
    this.expAct.dlg=true;
    this.expAct.no=no;
},
exp_do() {
    var dta=copyObj(this.expAct.dta,['day','descr']);
    dta.start=parseInt(datetimeToDate(this.expAct.dta.realStart_s).getTime()/60000);
    dta.end=parseInt(datetimeToDate(this.expAct.dta.realEnd_s).getTime()/60000);
    request({method:"PUT", url:"/exception/commit", data:dta}, this.ibf.SERVICE_HR).then(resp => {
        if(resp.code != RetCode.OK) {
            this.$refs.alertDlg.showErr(resp.code, resp.info);
            return;
        }
        this.expAct.dlg=false;
        this.expAct.no=-1;
        this.query_exps();
    });
},
hasOverlap(intervals) {
    intervals.sort((a,b) => a.start-b.start);
    for(let i=0; i<intervals.length-1; i++) {
        if(intervals[i].end>intervals[i+1].start) {
            return true;
        }
    }
    return false;
},
expdt2str(v,dt) {
    if(v<=0) return '00:00';
    dt.setTime(v*60000);
    var h=dt.getHours();
    var m=dt.getMinutes();
    return (h<10?('0'+h):h)+':'+(m<10?('0'+m):m);
}
},
template:`
<q-layout view="hHh lpr fFf">
  <q-header>
   <q-toolbar>
     <q-btn flat icon="arrow_back" dense @click="ibf.back()"></q-btn>
     <q-toolbar-title>{{tags.atd.title}}</q-toolbar-title>
     <q-btn flat icon="add_circle" dense @click="show_add()" v-show="tab!='exp'"></q-btn>
   </q-toolbar>
  </q-header>
  <q-footer>
   <q-tabs v-model="tab" @update:model-value="tab_changed"
   dense align="justify" switch-indicator inline-label
   class="text-grey bg-grey-3" active-color="primary" indicator-color="primary">
    <q-tab name="atd" icon="pending_actions" :label="tags.atd.ovOrLv"></q-tab>
    <q-tab name="wt" icon="work_history" :label="tags.atd.worktime"></q-tab>
    <q-tab name="exp" icon="running_with_errors" :label="tags.atd.clockExp"></q-tab>
   </q-tabs>
  </q-footer>
  <q-page-container>
    <q-page class="q-pa-none">
<q-tab-panels v-model="tab" class="q-pa-none q-ma-none">
<q-tab-panel name="atd">
<q-list>
  <q-item v-for="(a,i) in atds" clickable @click="show_atd(i)">
    <q-item-section>
     <q-item-label>{{a.type_s}}</q-item-label>
     <q-item-label caption>{{a.at}}</q-item-label>
    </q-item-section>
    <q-item-section>
     <q-item-label>{{a.opinion}}</q-item-label>
     <q-item-label caption>{{a.cfmAcc}}</q-item-label>
    </q-item-section side>
    <q-item-section side>{{a.state_s}}</q-item-section>
  </q-item>
</q-list>
<div class="q-pa-sm flex flex-center" v-show="atdPg.max>1">
 <q-pagination v-model="atdPg.cur" color="primary" :max="atdPg.max" max-pages="10"
  boundary-numbers="false" @update:model-value="query_atds"></q-pagination>
</div>
</q-tab-panel>

<q-tab-panel name="wt">
<q-list>
 <q-item v-for="(w,i) in wts" clickable @click="show_wt(i)">
   <q-item-section>
    <q-item-label>{{w.prjName}}</q-item-label>
    <q-item-label caption>{{w.month_s}}</q-item-label>
   </q-item-section>
   <q-item-section>{{w.state_s}}</q-item-label>
    <q-item-label caption>{{w.cmt}}</q-item-label>
   </q-item-section>
   <q-item-section side>
    <q-item-label>{{w.cfmAcc}}</q-item-label>
    <q-item-label caption>{{w.at}}</q-item-label>
   </q-item-section>
 </q-item>
</q-list>
<div class="q-pa-sm flex flex-center" v-show="wtPg.max>1">
 <q-pagination v-model="wtPg.cur" color="primary" :max="wtPg.max" max-pages="10"
  boundary-numbers="false" @update:model-value="query_wts"></q-pagination>
</div>
</q-tab-panel>

<q-tab-panel name="exp">
<q-list>
  <q-item v-for="(e,i) in exps" clickable @click="show_exp(i)">
   <q-item-section>
    <q-item-label>{{e.day_s}}({{e.state_s}})</q-item-label>
    <q-item-label caption>{{e.start_s}} - {{e.end_s}}</q-item-label>
   </q-item-section>
   <q-item-section>
    <q-item-label>{{e.descr}}</q-item-label>
    <q-item-label caption>{{e.realStart_s}} - {{e.realEnd_s}}</q-item-label>
   </q-item-section>
   <q-item-section side>{{e.cfmAcc}}</q-item-section>
  </q-item>
</q-list>
</q-tab-panel>
</q-tab-panels>
    </q-page>
  </q-page-container>
</q-layout>

<alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" ref="alertDlg"></alert-dialog>

<q-dialog v-model="atdAct.dlg" persistent no-shake>
 <q-card style="min-width:70vw">
  <q-card-section>
   <div class="text-h6">{{tags.apply}} {{tags.atd.ovOrLv}}</div>
  </q-card-section>
  <q-card-section class="q-pt-none">
  <q-list>
    <q-item clickable v-for="(t,i) in atdAct.tms">
     <q-item-section>
      <q-item-label>{{t.type_s}}
       <q-icon color="red" name="clear" @click="rmv_atd_tm(i)" class="q-pl-md" v-if="atdAct.editable"></q-icon>
      </q-item-label>
      <q-item-label caption>{{t.start_s}}</q-item-label>
      <q-item-label caption>{{t.end_s}}</q-item-label>
     </q-item-section>
     <q-item-section side>{{t.cmt}}<q-item-section>
    </q-item>
  </q-list>
  <div v-if="atdAct.editable">
   <div class="row">
    <div class="col self-center"><q-separator></q-separator></div>
    <div class="col-1 text-right">
     <q-icon name="add_circle" color="orange" size="1.5em" @click="add_atd_tm"></q-icon>
    </div>
   </div>
   <div class="row">
    <div class="col">
     <datetime-input v-model="atdAct.tm.start" :label="tags.start"
      :format="tags.dateFmt" :showMinute="false"></datetime-input>
    </div>
    <div class="col-2 self-center text-center">
     <q-icon name="arrow_right_alt" size="2em"></q-icon>
    </div>
    <div class="col">
     <datetime-input v-model="atdAct.tm.end" :label="tags.end"
     :format="tags.dateFmt" :showMinute="false"></datetime-input>
    </div>
   </div>
   <div class="row">
    <div class="col-3 self-end q-pr-md">
     <q-select v-model="atdAct.tm.type" :options="tmTypes"
      dense map-options emit-value></q-select>
    </div>
    <div class="col">
     <q-input v-model="atdAct.tm.cmt" :label="tags.cmt"></q-input>
    </div>
   </div>
  </div>
  </q-card-section>
  <q-card-actions align="right">
    <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
    <q-btn flat :label="tags.remove" color="red" @click="remove_atd"
     v-if="atdAct.editable&&atdAct.no>-1"></q-btn>
    <q-btn :label="tags.ok" color="primary" @click="atd_do" v-if="atdAct.editable"></q-btn>
  </q-card-actions>
 </q-card>
</q-dialog>

<q-dialog v-model="wtAct.dlg" persistent no-shake>
 <q-card style="min-width:70vw">
  <q-card-section>
   <div class="row">
    <div class="text-h6 col">{{tags.atd.worktime}}</div>
    <div class="col">
     <month-input class="text-subtitle1 q-pl-sm text-primary" :disable="wtAct.no<0"
       v-model="wtAct.month" max="-1m"></month-input>
    </div>
   </div>
  </q-card-section>
  <q-card-section class="q-pt-none">
  <q-list>
   <q-item clickable v-for="(t,i) in wtAct.items">
     <q-item-section>
      <q-item-label>{{t.prjName}}
       <q-icon color="red" name="clear" @click="rmv_wt_item(i)" class="q-pl-md" v-if="wtAct.editable"></q-icon>
      </q-item-label>
      <q-item-label caption>{{t.ratio}}%</q-item-label>
     </q-item-section>
     <q-item-section>
      <q-item-label>{{t.state_s}}</q-item-label>
      <q-item-label caption>{{t.cmt}}</q-item-label>
     <q-item-section>
   </q-item>
  </q-list>
  <div v-if="wtAct.editable">
   <div class="row">
    <div class="col self-center"><q-separator></q-separator></div>
    <div class="col-1 text-right">
     <q-icon name="add_circle" color="orange" size="1.5em" @click="add_wt_item"></q-icon>
    </div>
   </div>
   <prj-input v-model="wtAct.wt.prj" :label="tags.atd.prj"></prj-input>
   <q-input v-model.number="wtAct.wt.ratio" :label="tags.atd.ratio">
    <template v-slot:append>
     <q-icon name="percent" color="primary"></q-icon>
    </template>
   </q-input>
   <q-input v-model="wtAct.wt.cmt" :label="tags.cmt" type="textarea" rows="2"></q-input>
  </div>
  </q-card-section>
  <q-card-actions align="right">
    <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
    <q-btn :label="tags.ok" color="primary" @click="wt_declare" v-if="wtAct.editable"></q-btn>
  </q-card-actions>
 </q-card>
</q-dialog>

<q-dialog v-model="expAct.dlg" persistent no-shake>
 <q-card style="min-width:70vw">
  <q-card-section>
   <div class="text-h6">{{tags.atd.clockExp}}</div>
   <div class="text-caption">{{expAct.dta.start_s}}-{{expAct.dta.end_s}}</div>
  </q-card-section>
  <q-card-section class="q-pt-none">
   <datetime-input v-model="expAct.dta.realStart_s" :label="tags.start"
    :format="tags.dateFmt" :showMinute="false"></datetime-input>
   <datetime-input v-model="expAct.dta.realEnd_s" :label="tags.end"
    :format="tags.dateFmt" :showMinute="false"></datetime-input>
   <q-input v-model="expAct.dta.descr" :label="tags.cmt" type="textarea" rows=2></q-input>
  </q-card-section>
  <q-card-actions align="right">
    <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
    <q-btn :label="tags.ok" color="primary" @click="exp_do"></q-btn>
  </q-card-actions>
 </q-card>
</q-dialog>
`
}