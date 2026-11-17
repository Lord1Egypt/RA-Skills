import AlertDialog from "/assets/v3/components/alert_dialog.js"
import MonthInput from "/assets/v3/components/month_input.js"
const STORAGE_DPMNO="dpmNo";
export default {
inject:["ibf"],
components:{
    "alert-dialog" : AlertDialog,
    "month-input":MonthInput
},
data() {return {
    tags:this.ibf.tags,
    tab:'applies',
    gid:0,
    gname:'',
    exps:[], //考勤异常列表申请
    perfs:[], //绩效查询
    applies:[], //加班、请假、工作日在途、工时申报
    levels:[], //绩效等级
    grpOpts:[],
    month:{v:0,cur:0,e:false/*绩效中是否有可修改的行*/},
    perfDlg:{obj:{},no:-2,show:false},//待编辑绩效
    expPg:{max:0,cur:1},
    perfPg:{max:0,cur:1,month:'-1m'},
    aplPg:{max:0,cur:1}
}},
created(){
    var dt=new Date();
    var cur=dt.getFullYear()*12+dt.getMonth();
    this.month={v:cur, cur:cur,e:false};

    var opts={method:"GET",url:"/config/listPerfLevel"};
    request(opts, this.ibf.SERVICE_HR).then(resp => {
        if(resp.code==RetCode.OK) {
            this.levels=resp.data.list;
        }
    });
    if(this.ibf.adminDpms.length>0){
        var dpmNo=storageGet(STORAGE_DPMNO,0);
        if(dpmNo>=this.ibf.adminDpms.length) {
            dpmNo=0;
        }
        this.gid=this.ibf.adminDpms[dpmNo].id;
        this.gname=this.ibf.adminDpms[dpmNo].name;
        this.query_exps(1);
        for(var dp of this.ibf.adminDpms) {
            this.grpOpts.push({value:dp.id,label:dp.path});
        }
    }
},
methods:{
tab_changed(tab) {
    if(tab=='exps') {
        if(this.exps.length==0) {
            this.query_exps(this.expPg.cur);
        }
    } else if(tab=='applies') {
        if(this.applies.length==0) {
            this.query_applies(this.aplPg.cur);
        }
    } else {
        if(this.perfs.length==0) {
            this.query_perfs(this.perfPg.cur);
        }
    }
},
query_applies(pg) {
    var offset=(parseInt(pg)-1)*this.ibf.N_PAGE;
    var url="/apply/waitApplies?offset="+offset+'&num='+this.ibf.N_PAGE+"&gid="+this.gid;
    request({method:"GET", url:url}, this.ibf.SERVICE_HR).then(resp => {
        if(resp.code!=RetCode.OK) {
            return;
        }
        //id,uid,account,at
        var dt=new Date();
        this.applies=resp.data.list.map(a=>{
            dt.setTime(a.at);
            a.at=date2str(dt);
            a.type=this.tags.atd.aplType[a.type];
            return a;
        });
        this.aplPg.max=Math.ceil(resp.data.total/this.ibf.N_PAGE);
    })
},
query_exps(pg) {
    var offset=(parseInt(pg)-1)*this.ibf.N_PAGE;
    var opts={method:"GET", url:"/exception/waitforme?offset="+offset+'&num='+this.ibf.N_PAGE+"&gid="+this.gid}
    request(opts, this.ibf.SERVICE_HR).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.exps=[];
            return;
        }
        var dt=new Date();
        this.exps=resp.data.list.map(e=>{
            if(e.start<=0) {
                e.start=this.tags.atd.notChked;
            } else {
                dt.setTime(e.start*60000);
                e.start=datetime2str(dt);
            }
            if(e.end<=0) {
                e.end=this.tags.atd.notChked;
            } else {
                dt.setTime(e.end*60000);
                e.end=datetime2str(dt);
            }
            dt.setTime(e.realStart*60000);
            e.realStart=datetime2str(dt);
            dt.setTime(e.realEnd*60000);
            e.realEnd=datetime2str(dt);
            return e;
        });
        this.expPg.max=Math.ceil(resp.data.total/this.ibf.N_PAGE);
    })
},
query_perfs(pg) {
    var offset=(parseInt(pg)-1)*this.ibf.N_PAGE;
    var url="/perf/list?offset="+offset+'&num='+this.ibf.N_PAGE+"&gid="+this.gid+"&month="+this.month.v;
    request({method:"GET", url:url}, this.ibf.SERVICE_HR).then(resp => {
        this.month.e=false;
        if(resp.code!=RetCode.OK) {
            this.perfs=[];
            this.perfPg.max=0;
            return;
        }
        var mbrs=resp.data.members;
        this.perfs=resp.data.list.map(p=>{
            var l=p.level==''?this.levels[0].level:p.level;
            if(p.cfmed=='N') this.month.e=true;
            var cmt=p.cmt==''?this.tags.grp.perfCmt:p.cmt;
            var mbr=mbrs[p.uid];
            return {uid:p.uid,level:l,account:mbr[0],
                name:mbr[1],cmt:cmt,cfmed:p.cfmed};
        });
        this.perfPg.max=Math.ceil(resp.data.total/this.ibf.N_PAGE);
    })
},
cfm_perf() {
    var opts={method:"PUT",url:"/api/perf/confirm", data:{gid:this.gid,month:this.month.v}};
    request(opts, this.ibf.SERVICE_HR).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.$refs.alertDlg.showErr(resp.code, resp.info);
            return;
        }
        this.query_perfs(this.perfPg.cur);
    });
},
cfm_exp(uid,day) {
    var opts={method:"PUT",url:"/api/exception/confirm", data:{uid:uid,day:day}};
    request(opts, this.ibf.SERVICE_HR).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.$refs.alertDlg.showErr(resp.code, resp.info);
            return;
        }
        this.query_exps(this.expPg.cur);
    }); 
},
rej_exp(uid,day) {
    var opts={method:"PUT",url:"/api/exception/reject", data:{uid:uid,day:day}};
    request(opts, this.ibf.SERVICE_HR).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.$refs.alertDlg.showErr(resp.code, resp.info);
            return;
        }
        this.query_exps(this.expPg.cur);
    }); 
},
set_month(ym) {
    this.month.v=ym.num;
    this.query_perfs(this.perfPg.cur);
},
init_perf() {
    var opts={method:"POST",url:"/api/perf/init", data:{gid:this.gid,month:this.month.v}};
    request(opts, this.ibf.SERVICE_HR).then(resp => {
        if(resp.code!=RetCode.OK) {
            return;
        }
        this.query_perfs(this.perfPg.cur);
    });
},
clear_perf() {
    var opts={method:"DELETE",url:"/api/perf/clear?gid="+this.gid+"&month="+this.month.v};
    request(opts, this.ibf.SERVICE_HR).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.$refs.alertDlg.showErr(resp.code, resp.info);
            return;
        }
        this.query_perfs(this.perfPg.cur);
    });
},
show_perf(i) {
    copyObjTo(this.perfs[i], this.perfDlg.obj);
    this.perfDlg.show=true;
    this.perfDlg.no=i;
},
save_perf() {
    var dta=copyObj(this.perfDlg.obj,['uid','level','cmt','month']);
    dta.month=this.month.v;
    var opts={method:"PUT",url:"/api/perf/set", data:dta};
    request(opts, this.ibf.SERVICE_HR).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.$refs.alertDlg.showErr(resp.code, resp.info);
        }
        copyObjTo(this.perfDlg.obj, this.perfs[this.perfDlg.no]);
        this.perfDlg.show=false;
        this.perfDlg.no=-2;
    });
},
change_grp(v){
    for(var i in this.ibf.adminDpms) {
        var dp=this.ibf.adminDpms[i];
        if(v==dp.id) {
            this.gid=dp.id;
            this.gname=dp.name;
            storageSet(STORAGE_DPMNO, i);
            break;
        }
    }
    this.exps=[];
    this.applies=[];
    this.perfs=[];
    this.tab_changed(this.tab);
    this.$refs.grpSelect.hide();
}
},
template:`
<q-layout view="hHh lpr fFf">
  <q-header>
   <q-toolbar>
     <q-btn flat icon="arrow_back" dense @click="ibf.back()"></q-btn>
     <q-toolbar-title>{{tags.grp.department}}-{{gname}}</q-toolbar-title>
     <q-btn flat icon="bookmarks" dense>
      <q-popup-proxy class="q-pa-md" ref="grpSelect">
       <q-option-group :options="grpOpts" type="radio" v-model="gid"
        @update:model-value="change_grp"></q-option-group>
      </q-popup-proxy>
     </q-btn>
   </q-toolbar>
  </q-header>
  <q-footer>
   <q-tabs v-model="tab" @update:model-value="tab_changed"
   dense align="justify" switch-indicator inline-label
    class="text-grey bg-grey-3" active-color="primary" indicator-color="primary">
    <q-tab name="applies" icon="pending_actions" :label="tags.grp.atd"></q-tab>
    <q-tab name="exps" icon="running_with_errors" :label="tags.grp.clockExp"></q-tab>
    <q-tab name="perfs" icon="abc" :label="tags.grp.perf"></q-tab>
   </q-tabs>
  </q-footer>
  <q-page-container>
    <q-page class="q-pa-none">
<q-tab-panels v-model="tab">
<q-tab-panel name="applies">
<q-list>
  <q-item v-for="a in applies">
    <q-item-section>{{a.account}}</q-item-section>
    <q-item-section>{{a.type}}</q-item-section>
    <q-item-section>{{a.at}}</q-item-section>
  </q-item>
</q-list>
<div class="q-pa-sm flex flex-center" v-show="aplPg.max>1">
 <q-pagination v-model="aplPg.cur" color="primary" :max="aplPg.max" max-pages="10"
  boundary-numbers="false" @update:model-value="query_applies"></q-pagination>
</div>
</q-tab-panel>

<q-tab-panel name="busi">
<q-list>
  <q-item v-for="b in business">
    <q-item-section>{{a.account}}</q-item-section>
    <q-item-section>{{a.type}}</q-item-section>
    <q-item-section>{{a.at}}</q-item-section>
  </q-item>
</q-list>
<div class="q-pa-sm flex flex-center" v-show="mbrPg.max>1">
 <q-pagination v-model="mbrPg.cur" color="primary" :max="mbrPg.max" max-pages="10"
  boundary-numbers="false" @update:model-value="query_members"></q-pagination>
</div>
</q-tab-panel>

<q-tab-panel name="exps">
<q-list>
  <q-item v-for="e in exps">
   <q-item-section>
    <q-item-label>{{e.account}}</q-item-label>
    <q-item-label caption>{{e.descr}}</q-item-label>
   </q-item-section>
   <q-item-section>
    <q-item-label>{{e.realStart}}</q-item-label>
    <q-item-label caption>{{e.start}}</q-item-label>
   </q-item-section>
   <q-item-section>
    <q-item-label>{{e.realEnd}}</q-item-label>
    <q-item-label caption>{{e.end}}</q-item-label>
   </q-item-section>
   <q-item-section side class="text-primary">
     <q-btn @click="cfm_exp(e.uid,e.day)" :label="tags.confirm" flat dense></q-btn>
     <q-btn @click="rej_exp(e.uid,e.day)" :label="tags.reject" flat dense></q-btn>
   </q-item-section>
  </q-item>
</q-list>
</q-tab-panel>

<q-tab-panel name="perfs" class="q-pa-none">
<div class="row justify-start bg-grey-3 text-primary q-pa-none">
  <div class="col-5 self-center">
   <month-input class="text-subtitle1 q-pl-sm" v-model="perfPg.month"
    @update:modelValue="set_month" min="-3" max="-1m"></month-input>
  </div>
  <div class="col self-center">
   <q-btn @click="init_perf" flat :label="tags.init"></q-btn>
  </div>
  <div class="col self-center" v-if="month.e">
    <q-btn @click="clear_perf" flat :label="tags.clear"></q-btn>
  </div>
  <div class="col self-center q-pr-sm" v-if="month.e">
   <q-btn @click="cfm_perf" flat :label="tags.submit"></q-btn>
  </div>
</div>
<div class="q-pa-sm flex flex-center" v-show="perfPg.max>1">
 <q-pagination v-model="perfPg.cur" color="primary" :max="perfPg.max" max-pages="10"
  boundary-numbers="false" @update:model-value="query_perfs"></q-pagination>
</div>
<q-list>
  <q-item v-for="(p,i) in perfs" :clickable="p.cfmed=='N'" @click="show_perf(i)">
   <q-item-section>{{p.account}}/{{p.name}}</q-item-section>
   <q-item-section :class="p.cfmed=='N'?'text-deep-orange':''" >
    {{p.level}}
   </q-item-section>
   <q-item-section>{{p.cmt}}</q-item-section>
  </q-item>
</q-list>
</q-tab-panel>
</q-tab-panels>
    </q-page>
  </q-page-container>
</q-layout>

<q-dialog v-model="perfDlg.show">
 <q-card style="min-width:70vw">
  <q-card-section>
      <div class="text-h6">{{perfDlg.account}}</div>
  </q-card-section>
  <q-card-section class="q-pt-none">
   <q-radio v-model="perfDlg.obj.level"
    v-for="l in levels" :val="l.level" :label="l.name"></q-radio>
   <q-input color="accent" v-model="perfDlg.obj.cmt" type="textarea" rows="2"
    dense autofocus></q-input>
  </q-card-section>
  <q-card-actions align="right">
  <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
     <q-btn :label="tags.ok" color="primary" @click="save_perf"></q-btn>
  </q-card-actions>
 </q-card>
</q-dialog>

<alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" ref="alertDlg"></alert-dialog>
`
}