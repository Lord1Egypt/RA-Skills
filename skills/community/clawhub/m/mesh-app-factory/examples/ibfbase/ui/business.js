import AlertDialog from "/assets/v3/components/alert_dialog.js";
import DatetimeInput from "/assets/v3/components/datetime_input.js";
import {datetimeToDate} from '/assets/v3/components/datetime_input.js';
import {addrToStr} from '/assets/v3/components/addr_input.js';
import {sta2icon} from '/assets/v3/components/workflow.js';
import AddrInput from "/assets/v3/components/addr_input.js";
import PrjInput from "./components/prj_selector.js";

const EMPTY_BUSI={prj:0,cfmAcc:'',cmt:'',reason:'',dest:'',start:'',end:''}
export default {
inject:["ibf"],
components:{
    "alert-dialog":AlertDialog,
    "datetime-input":DatetimeInput,
    "addr-input":AddrInput,
    "prj-input":PrjInput
},
data() {return {
    tags:this.ibf.tags,
    busis:[], //差旅记录
    busiPg:{max:0,cur:1},
    busiAct:{dlg:false,dta:{}}
}},
created(){
    this.query_busis(1);
},
methods:{
query_busis(pg) {
    var offset=(parseInt(pg)-1)*this.ibf.N_PAGE;
    var url="/business/my?offset="+offset+"&num="+this.ibf.N_PAGE;
    request({method:"GET", url:url}, this.ibf.SERVICE_BUSINESS).then(resp => {
        if(resp.code!=RetCode.OK) {
            return;
        }
        //id,pid,status,start,end,overAt,prjName,expense,subsidy,dest,reason,power
        var dt=new Date();
        this.busis=resp.data.list.map(b=>{
            if(b.overAt>0) {
                dt.setTime(b.overAt);
                b.overAt=date2str(dt);
            } else {
                b.overAt='';
            }
            dt.setTime(b.start*60000);
            b.start_s=datetime2str(dt);
            dt.setTime(b.end*60000);
            b.end_s=datetime2str(dt);
            b.status=sta2icon(b.status);
            return b;
        });
        this.busiPg.max=Math.ceil(resp.data.total/this.ibf.N_PAGE);
    })
},
show_add() {
    this.busiAct.dlg=true;
    copyObjTo(EMPTY_BUSI,this.busiAct.dta);
},
busi_do() {
    var busi=this.busiAct.dta;
    var dta=copyObj(busi,['dest','reason','cmt']);
    dta.pid=busi.prj.id;
    dta.start=parseInt(datetimeToDate(busi.start).getTime()/60000);
    dta.end=parseInt(datetimeToDate(busi.end).getTime()/60000);
    dta.dest=addrToStr(busi.dest);
    request({method:"POST", url:"/business/create", data:dta}, this.ibf.SERVICE_BUSINESS).then(resp=>{
        if(resp.code != RetCode.OK) {
            this.$refs.alertDlg.showErr(resp.code, resp.info);
            return;
        }
        this.busiAct.dlg=false;
        this.query_busis(this.busiPg.cur);
    });
}
},
template:`
<q-layout view="hHh lpr fFf">
  <q-header>
   <q-toolbar>
     <q-btn flat icon="arrow_back" dense @click="ibf.back()"></q-btn>
     <q-toolbar-title>{{tags.busi.title}}</q-toolbar-title>
     <q-btn flat icon="add_circle" dense @click="show_add"></q-btn>
   </q-toolbar>
  </q-header>
  <q-page-container>
    <q-page class="q-pa-md">
<q-list separator>
  <q-item v-for="b in busis" clickable @click="ibf.goto('/ibf/busidtl?id='+b.id)">
    <q-item-section>
     <q-item-label>{{b.prjName}}</q-item-label>
     <q-item-label caption>{{b.reason}}</q-item-label>
    </q-item-section>
    <q-item-section>
     <q-item-label>{{b.dest}}</q-item-label>
     <q-item-label caption>{{b.start_s}}-&gt;{{b.end_s}}</q-item-label>
    </q-item-section>
    <q-item-section thumbnail>
     <q-icon :name="b.status" color="primary" size="xs"></q-icon>
    </q-item-section>
  </q-item>
</q-list>
<div class="q-pa-sm flex flex-center" v-show="busiPg.max>1">
 <q-pagination v-model="busiPg.cur" color="primary" :max="busiPg.max" max-pages="10"
  boundary-numbers="false" @update:model-value="query_busis"></q-pagination>
</div>
    </q-page>
  </q-page-container>
</q-layout>

<alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" ref="alertDlg"></alert-dialog>

<q-dialog v-model="busiAct.dlg">
 <q-card style="min-width:70vw">
  <q-card-section>
   <div class="text-h6">{{tags.add}}</div>
  </q-card-section>
  <q-card-section class="q-pt-none">
   <prj-input v-model="busiAct.dta.prj" :label="tags.busi.prj"></prj-input>
   <datetime-input v-model="busiAct.dta.start" :label="tags.start"
    :format="tags.dateFmt" :showMinute="false"></datetime-input>
   <datetime-input v-model="busiAct.dta.end" :label="tags.end"
    :format="tags.dateFmt" :showMinute="false"></datetime-input>
   <addr-input v-model="busiAct.dta.dest" :label="tags.busi.dest"></addr-input>
   <q-input v-model="busiAct.dta.reason" :label="tags.busi.reason"></q-input>
   <q-input v-model="busiAct.dta.cmt" :label="tags.cmt" type="textarea" rows="2"></q-input>
  </q-card-section>
  <q-card-actions align="right">
    <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
    <q-btn :label="tags.ok" color="primary" @click="busi_do"></q-btn>
  </q-card-actions>
 </q-card>
</q-dialog>
`
}