import Workflow from "/assets/v3/components/workflow.js"
import AlertDialog from "/assets/v3/components/alert_dialog.js";
import ConfirmDialog from "/assets/v3/components/confirm_dialog.js"
import {_WF_} from "/assets/v3/components/workflow.js"
import Language from "./language.js"

//workflow会在其他服务中打开，不可以注入tags、service，所以单独加载，组件也需要单独加载
const sole_tags = Platform.language().indexOf("zh") == 0 ? Language.zh : Language.en;
const _SEGS_={ //不放在data中是为了避免不必要的双向绑定
  entry:[
    {t:'s',n:"office"},
    {t:'s',n:"worktime"},
    {t:'s',n:'email'},
    {t:'n',n:'quali'},
    {t:'n',n:'post'},
    {t:'n',n:'salary'},
    {t:'n',n:'dSalary'},
    {t:'n',n:'hSalary'},
    {t:'n',n:'subsidy'},
    {t:'d',n:'entryAt'},
    {t:'s',n:'addr'},
    {t:'s',n:'idno'}
  ],
  leave:[
    {t:'f',n:'state',f:null},
  ],
  grade:[
    {t:'n',n:'quali'},
    {t:'n',n:'post'},
    {t:'n',n:'subsidy'}
  ],
  stock:[
    {t:'n',n:'stock'}
  ],
  salary:[
    {t:'n',n:'salary'},
    {t:'n',n:'dSalary'},
    {t:'n',n:'hSalary'}
  ]
};
//处理salary,grade,stock三种工作流
export default {
inject:['ibf'],
components:{
    "confirm-dialog":ConfirmDialog,
    "alert-dialog":AlertDialog,
    "workflow":Workflow
},
data() {return {
    flowid:this.$route.query.flow,
    did:this.$route.query.did,
    alertDlg:null,
    tags:sole_tags,
    segments:[],
    curStep:0,
    info:{account:'',name:'',list:[],dlg:false}, //用于显示详情标题
    dtl:[],
    flow:{}//流程定义信息{name,maxStep,steps}
}},
created(){
    _WF_.flowDef(this.flowid).then(fd=>{
        this.flow=fd;

        var tags=this.tags;
        var eTags=tags.employee;
        if(fd.name=='leave') {
            _SEGS_.leave[0].f=(v)=>{
                return tags.evtType[v];
            }
        }

        var segments=_SEGS_[fd.name];
        for(var s of segments) { //初始化标签
            s.s=eTags[s.n];
        }
        this.segments=segments;
        this.get();
    });
},
mounted(){//不能在created中赋值，更不能在data中
    this.alertDlg=this.$refs.errMsg;
},
methods:{
get() {
    request({method:"GET",url:"/wfemployee/get?id="+this.did}, this.ibf.SERVICE_HR).then(resp=>{
        if(resp.code!=RetCode.OK) {
            if(resp.code==RetCode.NOT_EXISTS) {
                this.removeWf();
            }
            return;
        }
        var dta=copyObjExc(resp.data, ['data']);
        copyObjTo(JSON.parse(resp.data.data), dta);
        this.dtl=_WF_.formDtlData(dta, this.segments);
        this.info.account=dta.account; //入职时无employee，但是请求数据resp.data.data中有

        var tags=this.tags;
        var eTags=tags.employee;
        var p=resp.data; //maxEdu,firstEdu,sex,birth,name,phone
        this.info.name=p.name+' '+tags.sex[p.sex];

        var info=[];
        info.push({k:tags.pub.phone, v:p.phone});
        info.push({k:eTags.maxEdu, v:tags.edu[p.maxEdu]});
        info.push({k:eTags.firstEdu, v:tags.edu[p.firstEdu]});
        var dt=new Date();
        var thisYear=dt.getFullYear();
        dt.setTime(p.birth*60000);
        var birth=date2str(dt)+'('+(thisYear-dt.getFullYear())+')';
        info.push({k:tags.pub.birth, v:birth});

        var e=resp.data;
        if(e.salary) { //帐号已存在，比如离职、调薪等
            var segs=['office','worktime','account',
                'salary','dSalary','hSalary','subsidy','stock',
                'quali','post','addr','email'];
            dt.setTime(e.entryAt*60000);
            info.push({k:eTags.entryAt, v:date2str(dt)});
            info.push({k:eTags.state, v:tags.empState[e.state]});
            for(var i of segs) {
                info.push({k:eTags[i], v:e[i]});
            }
        }
        this.info.list=info;
    })
},
removeWf() { //数据不存在，工作流数据错乱的情况下，删除工作流记录
    if(this.curStep>0)return;//只有第0步权签人(创建人)才有权限删除

    this.$refs.confirmDlg.show(this.tags.wrongFlowState, ()=>{
        _WF_.remove(this.flowid, this.did, this.ibf.SERVICE_HR).then(resp=>{
            if(resp.code!=RetCode.OK) {
                this.$refs.errMsg.showErr(resp.code, resp.info);
            }else{
                this.ibf.back();
            }
        })
    })
},
remove() {
    request({method:"DELETE",url:"/wfemployee/remove?did="+this.did}, this.ibf.SERVICE_HR).then(resp=>{
        if(resp.code!=RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.ibf.back();
    })
}
},
template:`
<q-layout view="hHh lpr fFf">
  <q-header>
   <q-toolbar>
    <q-btn flat icon="arrow_back" dense @click="ibf.back"></q-btn>
    <q-toolbar-title>{{flow.dispName}}</q-toolbar-title>
    <q-btn flat icon="cancel" dense v-if="curStep<=0" @click="remove"></q-btn>
    <q-btn flat icon="person_pin_circle" dense @click="info.dlg=true"></q-btn>
   </q-toolbar>
  </q-header>
  <q-page-container>
    <q-page class="q-pa-sm">
<q-list dense>
  <q-item>
    <q-item-section>{{tags.employee.account}}</q-item-section>
    <q-item-section side>{{info.account}}</q-item-section>
  </q-item>
  <q-item>
    <q-item-section>{{tags.pub.name}}</q-item-section>
    <q-item-section side>{{info.name}}</q-item-section>
  </q-item>
  <q-item v-for="d in dtl">
    <q-item-section>{{d.k}}</q-item-section>
    <q-item-section side>{{d.v}}</q-item-section>
  </q-item>
</q-list>
<q-separator color="primary" inset></q-separator>
<workflow :service="ibf.SERVICE_HR" :flowid="flowid" :did="did"
 :flowTags="tags.flowTags" :alertDlg="alertDlg" v-model="curStep"></workflow>
    </q-page>
  </q-page-container>
</q-layout>

<q-dialog v-model="info.dlg">
  <q-card style="min-width:70vw">
    <q-card-section>
      <div class="text-h6">{{info.name}}</div>
    </q-card-section>
    <q-card-section class="q-pt-none">
    <q-list dense>
      <q-item v-for="i in info.list" dense>
        <q-item-section>{{i.k}}</q-item-section>
        <q-item-section>{{i.v}}</q-item-section>
      </q-item>
    </q-list>
    </q-card-section>
  </q-card>
</q-dialog>
    
<alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" ref="errMsg"></alert-dialog>
<confirm-dialog :title="tags.alert" :close="tags.cancel" :ok="tags.ok" ref="confirmDlg"></confirm-dialog>
`
}